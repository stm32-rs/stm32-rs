use std::env;
use std::fs;
use std::path::PathBuf;
fn main() {
    if env::var_os("CARGO_FEATURE_RT").is_some() {
        let out = &PathBuf::from(env::var_os("OUT_DIR").unwrap());
        println!("cargo:rustc-link-search={}", out.display());
        let device_file = if env::var_os("CARGO_FEATURE_STM32G030").is_some() {
            "src/stm32g030/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32G031").is_some() {
            "src/stm32g031/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32G041").is_some() {
            "src/stm32g041/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32G07X").is_some() {
            "src/stm32g07x/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32G081").is_some() {
            "src/stm32g081/device.x"
        } else { panic!("No device features selected"); };
        fs::copy(device_file, out.join("device.x")).unwrap();
        println!("cargo:rerun-if-changed={}", device_file);
    }
    println!("cargo:rerun-if-changed=build.rs");
}
