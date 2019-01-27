extern crate svd2rust;
extern crate zip;

use std::env;
use std::fs::File;
use std::io::{self, Read, Write};
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};

fn main() {
    let mut features: std::collections::HashSet<_> = std::env::vars()
        .filter_map(|var| {
            const FEATURE_PREFIX: &str = "CARGO_FEATURE_";
            match var {
                (ref key, _) if key.starts_with(FEATURE_PREFIX) => {
                    Some(String::from(&key[FEATURE_PREFIX.len()..]))
                }
                _ => None,
            }
        })
        .collect();
    let _feat_default = features.remove("DEFAULT");
    let feat_patch = features.remove("PATCH");

    let feat_fmt = features.remove("FMT");
    let feat_nightly = features.remove("NIGHTLY");

    let _feat_rt = features.remove("RT");
    let _feat_cmrt = features.remove("CORTEX_M_RT");

    match features.len() {
        0 => panic!("A device feature must be specified. example: --features stm32f303"),
        1 => (),

        // Note: The compilation will fail due to multiply defined
        // static variables (ex: DEVICE_PERIPHERALS) if more then
        // one device feature is specified.
        _ => panic!("Only one device feature can be specified"),
    }

    for feature in features.iter().take(1) {
        let svd_filename = format!("{}.svd", feature);
        let mut svd = get_svd(&svd_filename).expect(&format!("Unable to find {}", svd_filename));

        if feat_patch {
            let feat_lower = feature.to_lowercase();
            let cfg_path = Path::new("devices").join(format!("{}.yaml", feat_lower));
            svd = patch_svd(cfg_path.to_str().unwrap(), &svd)
                .expect(&format!("Unable to patch {}", svd_filename));
        }

        let mod_path = Path::new("src").join("lib.rs");
        std::fs::DirBuilder::new()
            .recursive(true)
            .create(mod_path.parent().unwrap())
            .expect("Unable to create src dir");

        let svd2rust::Generation {
            lib_rs,
            device_specific,
            ..
        } = svd2rust::generate(&svd, &svd2rust::Target::CortexM, feat_nightly)
            .expect("Failed to generate rust library");

        File::create(&mod_path)
            .unwrap()
            .write_all(lib_rs.as_bytes())
            .expect("Unable to write module");

        let mut out = &PathBuf::from(env::var("OUT_DIR").unwrap());
        println!("cargo:rustc-link-search={}", out.display());
        File::create(out.join("device.x"))
            .unwrap()
            .write_all(device_specific.unwrap().device_x.as_bytes())
            .expect("Unable to write device.x");

        if feat_fmt {
            Command::new("rustfmt")
                .args(&["--write-mode", "overwrite"])
                .arg(&mod_path)
                .output()
                .expect("Unable to format module");
        }
    }
}

fn get_svd(filename: &str) -> io::Result<String> {
    for entry in std::fs::read_dir(Path::new("svd").join("vendor"))? {
        let path = entry?.path();

        if let Ok(file) = File::open(path) {
            if let Ok(mut archive) = zip::ZipArchive::new(file) {
                for i in 0..archive.len() {
                    if let Ok(mut file) = archive.by_index(i) {
                        if file.name().ends_with(filename) {
                            let mut buf = String::new();
                            file.read_to_string(&mut buf)?;
                            return Ok(buf);
                        }
                    }
                }
            }
        }
    }
    Err(io::Error::new(io::ErrorKind::NotFound, ""))
}

fn patch_svd(filename: &str, svd_data: &str) -> io::Result<String> {
    let patch_path = Path::new("scripts").join("svdpatch.py");
    let mut python = Command::new("python3")
        .arg(patch_path.to_str().unwrap())
        .arg(filename)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()?;
    {
        let stdin = python.stdin.as_mut().expect("Unable to open stdin");
        stdin
            .write_all(svd_data.as_bytes())
            .expect("Unable to write to stdin");
    }

    Ok(String::from_utf8(
        python
            .wait_with_output()
            .expect("Unable to read from stdout")
            .stdout,
    )
    .expect("Unable to convert to string"))
}
