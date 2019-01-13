use std::env;
use std::fs;
use std::path::PathBuf;
fn main() {
    if env::var_os("CARGO_FEATURE_RT").is_some() {
        let out = &PathBuf::from(env::var_os("OUT_DIR").unwrap());
        println!("cargo:rustc-link-search={}", out.display());
        let device_file = if env::var_os("CARGO_FEATURE_STM32L4X1").is_some() {
            "src/stm32l4x1/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32L4X2").is_some() {
            "src/stm32l4x2/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32L4X3").is_some() {
            "src/stm32l4x3/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32L4X5").is_some() {
            "src/stm32l4x5/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32L4X6").is_some() {
            "src/stm32l4x6/device.x"
        } else { panic!("No device features selected"); };
        fs::copy(device_file, out.join("device.x")).unwrap();
        println!("cargo:rerun-if-changed={}", device_file);
    }
    println!("cargo:rerun-if-changed=build.rs");
}
