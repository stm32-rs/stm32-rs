use std::env;
use std::fs;
use std::path::PathBuf;
fn main() {
    if env::var_os("CARGO_FEATURE_RT").is_some() {
        let out = &PathBuf::from(env::var_os("OUT_DIR").unwrap());
        println!("cargo:rustc-link-search={}", out.display());
        let device_file = if env::var_os("CARGO_FEATURE_STM32F401").is_some() {
            "src/stm32f401/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F405").is_some() {
            "src/stm32f405/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F407").is_some() {
            "src/stm32f407/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F410").is_some() {
            "src/stm32f410/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F411").is_some() {
            "src/stm32f411/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F412").is_some() {
            "src/stm32f412/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F413").is_some() {
            "src/stm32f413/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F427").is_some() {
            "src/stm32f427/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F429").is_some() {
            "src/stm32f429/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F446").is_some() {
            "src/stm32f446/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F469").is_some() {
            "src/stm32f469/device.x"
        } else { panic!("No device features selected"); };
        fs::copy(device_file, out.join("device.x")).unwrap();
        println!("cargo:rerun-if-changed={}", device_file);
    }
    println!("cargo:rerun-if-changed=build.rs");
}
