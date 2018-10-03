//! Peripheral access API for STM32F3 microcontrollers
//! (generated using [svd2rust](https://github.com/rust-embedded/svd2rust)
//! 0.13.1)
//!
//! You can find an overview of the API here:
//! https://docs.rs/svd2rust/0.13.1/svd2rust/#peripheral-api
//!
//! For more details see the README here:
//! https://github.com/adamgreig/stm32-rs
//!
//! This crate supports all STM32F3 devices; for the complete list please
//! see:
//! https://github.com/adamgreig/stm32-rs/tree/master/STM32F3
//!
//! Due to doc build limitations, not all devices may be shown on docs.rs;
//! a representative few have been selected instead. For a complete list of
//! available registers and fields see: https://stm32.agg.io/rs

#![allow(non_camel_case_types)]
#![no_std]

extern crate vcell;
extern crate bare_metal;
extern crate cortex_m;

#[cfg(feature = "rt")]
extern crate cortex_m_rt;

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

