use std::env;
use std::fs;
use std::path::PathBuf;
fn main() {
    if env::var_os("CARGO_FEATURE_RT").is_some() {
        let out = &PathBuf::from(env::var_os("OUT_DIR").unwrap());
        println!("cargo:rustc-link-search={}", out.display());
        let device_file = if env::var_os("CARGO_FEATURE_STM32F0X0").is_some() {
            "src/stm32f0x0/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F0X1").is_some() {
            "src/stm32f0x1/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F0X2").is_some() {
            "src/stm32f0x2/device.x"
        } else if env::var_os("CARGO_FEATURE_STM32F0X8").is_some() {
            "src/stm32f0x8/device.x"
        } else { panic!("No device features selected"); };
        fs::copy(device_file, out.join("device.x")).unwrap();
        println!("cargo:rerun-if-changed={}", device_file);
    }
    println!("cargo:rerun-if-changed=build.rs");
}
