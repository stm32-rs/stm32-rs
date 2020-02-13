//! Peripheral access API for STM32G4 microcontrollers
//! (generated using [svd2rust](https://github.com/rust-embedded/svd2rust)
//! 0.17.0)
//!
//! You can find an overview of the API here:
//! [svd2rust/#peripheral-api](https://docs.rs/svd2rust/0.17.0/svd2rust/#peripheral-api)
//!
//! For more details see the README here:
//! [stm32-rs](https://github.com/stm32-rs/stm32-rs)
//!
//! This crate supports all STM32G4 devices; for the complete list please
//! see:
//! [stm32g4](https://github.com/stm32-rs/stm32-rs/tree/master/stm32g4)
//!
//! Due to doc build limitations, not all devices may be shown on docs.rs;
//! a representative few have been selected instead. For a complete list of
//! available registers and fields see: [stm32-rs Device Coverage](https://stm32.agg.io/rs)

#![allow(non_camel_case_types)]
#![no_std]

mod generic;
pub use self::generic::*;

#[cfg(feature = "stm32g431")]
pub mod stm32g431;

#[cfg(feature = "stm32g441")]
pub mod stm32g441;

#[cfg(feature = "stm32g471")]
pub mod stm32g471;

#[cfg(feature = "stm32g473")]
pub mod stm32g473;

#[cfg(feature = "stm32g474")]
pub mod stm32g474;

#[cfg(feature = "stm32g483")]
pub mod stm32g483;

#[cfg(feature = "stm32g484")]
pub mod stm32g484;

