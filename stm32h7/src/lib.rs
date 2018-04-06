//! Peripheral access API for STM32H7 microcontrollers
//! (generated using [svd2rust])
//! [svd2rust]: https://github.com/japaric/svd2rust
//!
//! You can find an overview of the API here:
//! https://docs.rs/svd2rust/0.8.1/svd2rust/#peripheral-api
//!
//! For more details see the README here:
//! https://github.com/adamgreig/stm32-rs

#![allow(non_camel_case_types)]
#![allow(private_no_mangle_statics)]
#![feature(const_fn)]
#![feature(optin_builtin_traits)]
#![no_std]

#![cfg_attr(feature = "rt", feature(global_asm))]
#![cfg_attr(feature = "rt", feature(macro_reexport))]
#![cfg_attr(feature = "rt", feature(used))]

extern crate vcell;
extern crate bare_metal;
extern crate cortex_m;

#[macro_reexport(default_handler, exception)]
#[cfg(feature = "rt")]
extern crate cortex_m_rt;

#[cfg(feature = "stm32h7x3")]
pub mod stm32h7x3;

