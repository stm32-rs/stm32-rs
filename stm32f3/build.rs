use std::env;
use std::fs;
use std::path::PathBuf;
fn main() {
    if env::var_os("CARGO_FEATURE_RT").is_some() {
        let out = &PathBuf::from(env::var_os("OUT_DIR").unwrap());
        println!("cargo:rustc-link-search={}", out.display());
        let device_file = if env::var_os("CARGO_FEATURE_STM32F301").is_some() {
            "src/stm32f301/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F302").is_some() {
            "src/stm32f302/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F303").is_some() {
            "src/stm32f303/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F373").is_some() {
            "src/stm32f373/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F3X4").is_some() {
            "src/stm32f3x4/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F3X8").is_some() {
            "src/stm32f3x8/device.x"
        } else { panic!("No device features selected"); };
        fs::copy(device_file, out.join("device.x")).unwrap();
        println!("cargo:rerun-if-changed={}", device_file);
    }
    println!("cargo:rerun-if-changed=build.rs");
}
