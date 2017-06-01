//! Peripheral access API for STM32F2 microcontrollers
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

#[cfg(feature = "stm32f215")]
pub mod stm32f215;

#[cfg(feature = "stm32f217")]
pub mod stm32f217;

