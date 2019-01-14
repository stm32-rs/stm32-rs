use std::env;
use std::fs;
use std::path::PathBuf;
fn main() {
    if env::var_os("CARGO_FEATURE_RT").is_some() {
        let out = &PathBuf::from(env::var_os("OUT_DIR").unwrap());
        println!("cargo:rustc-link-search={}", out.display());
        let device_file = if env::var_os("CARGO_FEATURE_STM32F7X2").is_some() {
            "src/stm32f7x2/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F7X3").is_some() {
            "src/stm32f7x3/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F7X5").is_some() {
            "src/stm32f7x5/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F7X6").is_some() {
            "src/stm32f7x6/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F7X7").is_some() {
            "src/stm32f7x7/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F7X9").is_some() {
            "src/stm32f7x9/device.x"
        } else { panic!("No device features selected"); };
        fs::copy(device_file, out.join("device.x")).unwrap();
        println!("cargo:rerun-if-changed={}", device_file);
    }
    println!("cargo:rerun-if-changed=build.rs");
}
