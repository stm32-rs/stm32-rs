//! Peripheral access API for STM32F3 microcontrollers
//! (generated using [svd2rust])
//! [svd2rust]: https://github.com/japaric/svd2rust
//!
//! You can find an overview of the API here:
//! https://docs.rs/svd2rust/0.8.1/svd2rust/#peripheral-api
//!
//! For more details see the README here:
//! https://github.com/adamgreig/stm32-rs

#![feature(const_fn)]
#![feature(optin_builtin_traits)]
#![no_std]

extern crate cortex_m;
extern crate vcell;

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

