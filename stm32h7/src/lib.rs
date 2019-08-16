//! Peripheral access API for STM32H7 microcontrollers
//! (generated using [svd2rust](https://github.com/rust-embedded/svd2rust)
//! 0.15.0)
//!
//! You can find an overview of the API here:
//! [svd2rust/#peripheral-api](https://docs.rs/svd2rust/0.15.0/svd2rust/#peripheral-api)
//!
//! For more details see the README here:
//! [stm32-rs](https://github.com/stm32-rs/stm32-rs)
//!
//! This crate supports all STM32H7 devices; for the complete list please
//! see:
//! [stm32h7](https://github.com/stm32-rs/stm32-rs/tree/master/stm32h7)
//!
//! Due to doc build limitations, not all devices may be shown on docs.rs;
//! a representative few have been selected instead. For a complete list of
//! available registers and fields see: [stm32-rs Device Coverage](https://stm32.agg.io/rs)

#![allow(non_camel_case_types)]
#![no_std]

mod generic;
pub use self::generic::*;

#[cfg(feature = "stm32h743")]
pub mod stm32h743;

#[cfg(feature = "stm32h743v")]
pub mod stm32h743v;

#[cfg(feature = "stm32h747cm7")]
pub mod stm32h747cm7;

#[cfg(feature = "stm32h753")]
pub mod stm32h753;

#[cfg(feature = "stm32h753v")]
pub mod stm32h753v;

