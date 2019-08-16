use std::env;
use std::fs;
use std::path::PathBuf;
fn main() {
    if env::var_os("CARGO_FEATURE_RT").is_some() {
        let out = &PathBuf::from(env::var_os("OUT_DIR").unwrap());
        println!("cargo:rustc-link-search={}", out.display());
        let device_file = if env::var_os("CARGO_FEATURE_STM32H743").is_some() {
            "src/stm32h743/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32H743V").is_some() {
            "src/stm32h743v/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32H747CM7").is_some() {
            "src/stm32h747cm7/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32H753").is_some() {
            "src/stm32h753/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32H753V").is_some() {
            "src/stm32h753v/device.x"
        } else { panic!("No device features selected"); };
        fs::copy(device_file, out.join("device.x")).unwrap();
        println!("cargo:rerun-if-changed={}", device_file);
    }
    println!("cargo:rerun-if-changed=build.rs");
}
