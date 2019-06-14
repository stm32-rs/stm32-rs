use std::env;
use std::fs;
use std::path::PathBuf;
fn main() {
    if env::var_os("CARGO_FEATURE_RT").is_some() {
        let out = &PathBuf::from(env::var_os("OUT_DIR").unwrap());
        println!("cargo:rustc-link-search={}", out.display());
        let device_file = if env::var_os("CARGO_FEATURE_STM32G431").is_some() {
            "src/stm32g431/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32G441").is_some() {
            "src/stm32g441/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32G471").is_some() {
            "src/stm32g471/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32G473").is_some() {
            "src/stm32g473/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32G474").is_some() {
            "src/stm32g474/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32G483").is_some() {
            "src/stm32g483/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32G484").is_some() {
            "src/stm32g484/device.x"
        } else { panic!("No device features selected"); };
        fs::copy(device_file, out.join("device.x")).unwrap();
        println!("cargo:rerun-if-changed={}", device_file);
    }
    println!("cargo:rerun-if-changed=build.rs");
}
