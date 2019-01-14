use std::env;
use std::fs;
use std::path::PathBuf;
fn main() {
    if env::var_os("CARGO_FEATURE_RT").is_some() {
        let out = &PathBuf::from(env::var_os("OUT_DIR").unwrap());
        println!("cargo:rustc-link-search={}", out.display());
        let device_file = if env::var_os("CARGO_FEATURE_STM32L100").is_some() {
            "src/stm32l100/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32L151").is_some() {
            "src/stm32l151/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32L162").is_some() {
            "src/stm32l162/device.x"
        } else { panic!("No device features selected"); };
        fs::copy(device_file, out.join("device.x")).unwrap();
        println!("cargo:rerun-if-changed={}", device_file);
    }
    println!("cargo:rerun-if-changed=build.rs");
}
