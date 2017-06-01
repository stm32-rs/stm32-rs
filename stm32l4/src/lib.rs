//! Peripheral access API for STM32L4 microcontrollers
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

#[cfg(feature = "stm32l4x1")]
pub mod stm32l4x1;

#[cfg(feature = "stm32l4x2")]
pub mod stm32l4x2;

#[cfg(feature = "stm32l4x3")]
pub mod stm32l4x3;

#[cfg(feature = "stm32l4x5")]
pub mod stm32l4x5;

#[cfg(feature = "stm32l4x6")]
pub mod stm32l4x6;

