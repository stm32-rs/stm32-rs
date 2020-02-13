//! Peripheral access API for STM32F4 microcontrollers
//! (generated using [svd2rust](https://github.com/rust-embedded/svd2rust)
//! 0.17.0)
//!
//! You can find an overview of the API here:
//! [svd2rust/#peripheral-api](https://docs.rs/svd2rust/0.17.0/svd2rust/#peripheral-api)
//!
//! For more details see the README here:
//! [stm32-rs](https://github.com/stm32-rs/stm32-rs)
//!
//! This crate supports all STM32F4 devices; for the complete list please
//! see:
//! [stm32f4](https://github.com/stm32-rs/stm32-rs/tree/master/stm32f4)
//!
//! Due to doc build limitations, not all devices may be shown on docs.rs;
//! a representative few have been selected instead. For a complete list of
//! available registers and fields see: [stm32-rs Device Coverage](https://stm32.agg.io/rs)

#![allow(non_camel_case_types)]
#![no_std]

mod generic;
pub use self::generic::*;

#[cfg(feature = "stm32f401")]
pub mod stm32f401;

#[cfg(feature = "stm32f405")]
pub mod stm32f405;

#[cfg(feature = "stm32f407")]
pub mod stm32f407;

#[cfg(feature = "stm32f410")]
pub mod stm32f410;

#[cfg(feature = "stm32f411")]
pub mod stm32f411;

#[cfg(feature = "stm32f412")]
pub mod stm32f412;

#[cfg(feature = "stm32f413")]
pub mod stm32f413;

#[cfg(feature = "stm32f427")]
pub mod stm32f427;

#[cfg(feature = "stm32f429")]
pub mod stm32f429;

#[cfg(feature = "stm32f446")]
pub mod stm32f446;

#[cfg(feature = "stm32f469")]
pub mod stm32f469;

