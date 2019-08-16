//! Peripheral access API for STM32F3 microcontrollers
//! (generated using [svd2rust](https://github.com/rust-embedded/svd2rust)
//! 0.15.0)
//!
//! You can find an overview of the API here:
//! [svd2rust/#peripheral-api](https://docs.rs/svd2rust/0.15.0/svd2rust/#peripheral-api)
//!
//! For more details see the README here:
//! [stm32-rs](https://github.com/stm32-rs/stm32-rs)
//!
//! This crate supports all STM32F3 devices; for the complete list please
//! see:
//! [stm32f3](https://github.com/stm32-rs/stm32-rs/tree/master/stm32f3)
//!
//! Due to doc build limitations, not all devices may be shown on docs.rs;
//! a representative few have been selected instead. For a complete list of
//! available registers and fields see: [stm32-rs Device Coverage](https://stm32.agg.io/rs)

#![allow(non_camel_case_types)]
#![no_std]

mod generic;
pub use self::generic::*;

#[cfg(feature = "stm32f301")]
pub mod stm32f301;

#[cfg(feature = "stm32f302")]
pub mod stm32f302;

#[cfg(feature = "stm32f303")]
pub mod stm32f303;

#[cfg(feature = "stm32f373")]
pub mod stm32f373;

#[cfg(feature = "stm32f3x4")]
pub mod stm32f3x4;

#[cfg(feature = "stm32f3x8")]
pub mod stm32f3x8;

