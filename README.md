# Pocket Tools #

Some experimental tools for shellcode and binaries. For more info, you can reach me on twitter [@dmxinajeansuit](https://twitter.com/dmxinajeansuit)

### Newly Added - murkr0w ###

murkr0w is a tool for executing binaries from tweets. It's in the earliest stages of development at this time, and was included here for a [live stream](https://twitch.tv/n0pchan).

### Shellder ###

Shellder is a shellcode injector that works with minimal ELF binary templates for rapid testing and other applications. 

Shellder relies on binary files header structure to quickly create valid binaries without the need for a compiler or cross compiler. Payloads are passed in the form of base64 hashes of raw opcodes. Currently only supporting payloads of up to 255 bytes, but a more robust implementation is forthcoming. 

    EXAMPLE: python shellder.py -p McBIu9GdlpHQjJf/SPfbU1RfmVJXVF6wOw8F -t elf64-x86-64

* McBIu9GdlpHQjJf/SPfbU1RfmVJXVF6wOw8F contains a 27 byte payload that launches /bin/sh

* sAFIicdIx8aPAEAAsgsPBbA8SDH/DwVbXjBeXSB1ISEK contains a 33 byte payload of some ASCII art printed to STDOUT. Originally appearing at [n0.lol](http://n0.lol/bp/elfbinarymangling)

The -t flag is the architecture target for the shldr binary. A similar payload to launch /bin/sh targeting 32 bit ARM would look like this:

    python shellder.py -p AWCP4hb/L+FAQHhEDDBJQFJACycB3wEnAd8vL2Jpbi8vc2g= -t elf32-littlearm

Targets completed

* elf64-x86-64        [x86_64 - Linux General]
* elf32-littlearm     [RaspberryPi, ARMv6, ARMv7]

Targets in development

* elf32-i386          [x86 - Linux]
* elf32-i686          [x86 - Linux]
* elf64-littleaarch64 [Android 64-bit]
* win32               [Windows 32 Bit]
* win64               [Windows 64 Bit]

Assistance Desired

* elf64-powerpc
* macho               [OSX, Mach Kernel, Multiarch Support]
* DOS 16 bit
* AVR

If you would like to contribute, feel free to reach out!

More test shellcodes can be found at [shell-storm.org](http://shell-storm.org/shellcode/)

### Exeggutor ###

Formerly known as 'Misato'.

Exeggutor divides a binary in two byte chunks and creates one index of unique combinations. It then reiterates through the binary and creates a second index with the values from the first that correspond to their position in the binary when it is reconstructed.

The deconstructed binary is recreated into an executable by the script when run, allowing for simple portable obfuscation of binaries.

This program can be used with binaries created by Shellder.