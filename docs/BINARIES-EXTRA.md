# Extra binaries (optional)

Built DLLs that the open code PRs rely on but that no PR ships, plus the fork's
wider 64-bit stock-Wine module set. They are here only so the series can be
tested before the farms are rebuilt; if you rebuild them yourself (as after
#22), this PR can be closed without affecting any code PR. It is independent of
#28 and contains no file that #28 ships.

**Provenance.** Every file is copied unchanged from the 125hz fork's committed
farms at `integration/upstream-0926` (8e45bef); the SHA-256 values below match
those blobs, and the working copies they were taken from were checked against
them. The fork's WSL build rounds built them from the fork's own branches (wine
`integration/upstream-0926` be9ed8b and `research/madeira-d3d12` at 8e45bef).
Those branches contain the reviewed PR sources **plus** the fork's other work,
so these are not rebuilds of exactly the reviewed sources. The last column
names the fork commit that last changed each file.

**Not included:** `dockhost.exe` and `dock-notices.txt` (Madeira Dock), the
64-bit `crypt32.dll` (it carries a certificate-chain logging change that no PR
contains), the fork's other test programs (`badbuf-x64.exe`, `ctx-x64.exe`, the
`*-x86.exe` programs other than `wma-x86.exe`), the `nls/` code pages, and
everything #28 already ships.

276 files, 243056128 bytes.

| Group | Files |
|---|---:|
| Media for #33: winegstreamer (i386, aarch64, arm64ec), wmadmod, quartz, qasf, wmvcore, devenum, dsdmo, mfmediaengine, mf, mfreadwrite, msdmo, `wma-x86.exe` | 17 |
| XAudio2/XACT/X3DAudio/XAPOFX with the FAudio changes (#33, wine#2 and #4) | 70 |
| D3D12 for #32: d3d12, madeira_d3d12, dcomp, ktmw32 | 4 |
| DirectInput for #29 / wine#3: dinput, dinput8 | 4 |
| kernelbase for #35 / wine#5 | 2 |
| 64-bit farm breadth (stock modules, no PR) | 179 |

The two i386 files take effect only with #26/#28, which add the `i386-windows`
folder to the app; upstream's project does not reference that folder yet.
Commits are split by group, so a subset can be taken on its own.

"new" files do not exist upstream; "replaces upstream's" files overwrite a
tracked upstream binary.

| File | Arch | State | Bytes | SHA-256 | Serves | Source | Last changed in fork |
|---|---|---|---:|---|---|---|---|
| `bluetoothapis.dll` | aarch64 | new | 524288 | `257a502fda96e55168631e9f4122e1eb41b669551a20d38b1d4de0f44ae68563` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `comctl32_v6.dll` | aarch64 | new | 1835008 | `0b4d9c779ad9ad7c5eb18e72c8b1491cd3968b6b104055958e86bfbb4c52b0b9` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `concrt140.dll` | aarch64 | replaces upstream's | 589824 | `5894429557cf61c85a4510c20f1cc1ef32a9ab08294ebf3ed1cfc03a2f0b526d` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | e88266d (2026-09-19) |
| `d2d1.dll` | aarch64 | new | 1114112 | `d9d50ab6f198025f60de3dc1dfe1981767cb64a1bc430628a74d55d4185a4c12` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3d10.dll` | aarch64 | new | 720896 | `549dd251e81d6646d87a3713a6caf780909588da85286aa583c282a03181420b` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3d10_1.dll` | aarch64 | new | 524288 | `4a0ffa6393d4a4b735c3c13842af27a59869612d1190a69f940edbec2119e985` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_33.dll` | aarch64 | new | 655360 | `136d69cf187c588636085305544e028cee76c79d79f1d7f55a1205ee4975aeb5` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_34.dll` | aarch64 | new | 655360 | `b6fa7b8346eb2d93b6947616ab91818e1eede2feb92453f112ba7a0303035c4d` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_35.dll` | aarch64 | new | 655360 | `d155d35d7dbdc19a6e6c8fe5e4581acdc0e2767c93e47828e3df8d4e27eb10a8` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_36.dll` | aarch64 | new | 655360 | `e32fc38878e1ae1bace6a980af9a2412d0cf5d13f6cff5c34c38b27a44ee1db1` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_37.dll` | aarch64 | new | 655360 | `dca7a0c45727bbdf4602bfdbff2e89bcfe58bdae1c0e50424cc320eaaa085022` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_38.dll` | aarch64 | new | 655360 | `2765dc24e68f1ac4c56bd3ef1e8d0eb6a22373985fab957415c0c3b115c48953` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_39.dll` | aarch64 | new | 655360 | `f17759c800b70cefdd2dfdeda141128dd1d38bc78e97a8d103d072c7f64fa70a` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_40.dll` | aarch64 | new | 655360 | `74baabdc6bef6d93b52a43aac445f66d411dba84c5cc0d23562327305f28befb` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_41.dll` | aarch64 | new | 655360 | `a082f3d5bc0096f2036912d3962183472e060b3c0d5ae1b6a9e064eaf01f4787` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_42.dll` | aarch64 | new | 655360 | `2319301c72295bd23716900444553ac235e06cdd73c8b7d18afbdf82670c1d2e` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_43.dll` | aarch64 | new | 655360 | `83b3ec67ea848e8bc26be4306ab766f156511c5dea7b75de43d0e48a403a0ba7` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_46.dll` | aarch64 | new | 655360 | `3f2e0dca0b8a6edbe4b013b94b44eaa6f4e81d60edfa61fc0cfa864c22c510bd` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_47.dll` | aarch64 | new | 655360 | `3dc0d7726b5d9046bb6afa4a7d64c9772fc23e083c9ab90ec9e03c092a6d4844` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_33.dll` | aarch64 | new | 524288 | `16d64bc467fe5c79d69e20c4692d7646d058bc6888f226c8665f56cb6ff0ce21` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_34.dll` | aarch64 | new | 524288 | `dac73830fda286d940afa4b1bd92844f601624b2ea3634b0ba7e9e2baa7cf45e` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_35.dll` | aarch64 | new | 524288 | `6a00d16060f0e6d5479f6a2cd97a37844e0f13963f9f336fdd8e40116dd955d2` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_36.dll` | aarch64 | new | 524288 | `5d723dc8ffe1b097cb8ea13f10da4afab4bfcef4f5aae8d838711db7d11f311f` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_37.dll` | aarch64 | new | 524288 | `78bbe824dd37436180bec71fee413ea16044794bcd68fa6e43a1d62302f91162` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_38.dll` | aarch64 | new | 524288 | `f7363f1696459161b3de28c3c540be8a45cdeb5db77cfbc4b6fd8c8548dacf8e` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_39.dll` | aarch64 | new | 524288 | `04e2cb603050b830e4a05c105b894cab3c4b651e1d41adcb892d19f67e7295f0` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_40.dll` | aarch64 | new | 524288 | `b15691f66db710856453f07cf36a0a78f792d77224b682f444c15825678bb2ee` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_41.dll` | aarch64 | new | 524288 | `5865b090af73865ce9aa8911a75c7de15dd05dcd0da9a8611ec24d1a6066ad9a` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_42.dll` | aarch64 | new | 524288 | `c5e5a8f25811d8b3d20bc271c7aaff8a30ef622d86b776207c9638d717e470e7` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_43.dll` | aarch64 | new | 786432 | `41e69487af10f8f4a457743a50749d7d2c0c02197b5b6d0594c87dc0c72409fd` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx11_42.dll` | aarch64 | new | 524288 | `1cd5d73266db7d85b050aa0d376c76f252f4d73184285dd145950d593bb12640` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx11_43.dll` | aarch64 | new | 524288 | `ec96ff4b6b591dceffb3b2642230062b59ece94919d014b7138adf030c417f36` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_24.dll` | aarch64 | new | 1245184 | `d8f856e8ad81e96d2422fe1f951d3d34989d57631c607c060870c6fd651e90a6` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_25.dll` | aarch64 | new | 1245184 | `261289ef6bb1b8ae92121ec82fa90c2868f2629b56dbb3b101fbd9c2bff8ee91` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_26.dll` | aarch64 | new | 1245184 | `88e2b9fe33698cfc4e6856c1eac059a8c0069a32ca3d1e4db1d689894a7ff948` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_27.dll` | aarch64 | new | 1245184 | `b9c189aa752f06fd3acfe3d7e368b9d712469221668a89fd6c2c43836e87ab03` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_28.dll` | aarch64 | new | 1245184 | `3b2e49e057e449e67326abedae68c752cd656a7626b49f90a8debaad2e7c4e0f` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_29.dll` | aarch64 | new | 1245184 | `49f14313dae06351961b15cc846485b8e9f504825053217d7778e1639ebdaa3d` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_30.dll` | aarch64 | new | 1245184 | `b469e2545201ac73947aff656106bfb7dba35cc1cad66edd5cbeb5c5954e4b40` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_31.dll` | aarch64 | new | 1245184 | `12f98773599c8dafabe8f4e7f122b49173719072f48ac7d073cc8bc10d779fc4` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_32.dll` | aarch64 | new | 1245184 | `d10d81dfd2a72ab43ccec6a109ce85bd1f981112d1dcb1b8088df95306ad381c` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_33.dll` | aarch64 | new | 1245184 | `821a59b12e3d8a2d1a91e786ba57282c19acb253ad45a28d988d442e44e4d24f` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_34.dll` | aarch64 | new | 1245184 | `510f823fe28b912d7e804a7b6fa843d772fbb443e48730302fea7f7ed296eb9d` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_35.dll` | aarch64 | new | 1245184 | `5cf42a8f162b5c014bae9534e104e847fefa5cd48c3861756db20fbb39773145` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_36.dll` | aarch64 | new | 1245184 | `74bb0b0bd6d0bbb1de3ac2c7acd211ab86d7304dae6ac309178cb49182fdecf4` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_37.dll` | aarch64 | new | 1245184 | `5bf3fb4fae274645907c07733b5d695266d830e3fa7d3f44f095a93c73b39424` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_38.dll` | aarch64 | new | 1245184 | `606e5d2d774ebd11e9056aa6b7c33d4ecb149a982c485ce0f502bfd7b88d45f3` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_39.dll` | aarch64 | new | 1245184 | `66a6d42109e88524da8f1ccbdf7514aa46e12829800d875e8fa30912439f3a92` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_40.dll` | aarch64 | new | 1245184 | `1e721fc736d6a4998413244ef2f267659d48b7998dc065c1405ada26aca96ef5` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_41.dll` | aarch64 | new | 1245184 | `07416ecd4380a519f6695a4baec3b1f4b5b5d0cf6e75d6c6cc4d3d4d1c06b42f` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_42.dll` | aarch64 | new | 1245184 | `59340e2b4fa876b613d33d01d01caf6fd0d6052031f1a39162a81676219eee7c` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_43.dll` | aarch64 | new | 1245184 | `cc55de60f68e7c7eac7417e78d8bc3d57d1a4ee9b36742ea27cc8b9383abf6a0` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `d3dxof.dll` | aarch64 | new | 720896 | `86ce02fe49e7401877edd0044b026b999a0f19b23f024592b97fe6d0704dfd4e` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `ddraw.dll` | aarch64 | new | 1114112 | `e1f532a6d61c366c56459ad555d22a84c30a338dca893b668b3b9ed58d584325` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `dinput.dll` | aarch64 | new | 786432 | `119f1f7cf7fd041b58b42bd81b59ee34b6d39a2c08cb82c1369d9753945c3ba7` | #29 controllers | Wine, changed by willfaust/wine#3 | ad5e3a5 (2026-09-18) |
| `dinput8.dll` | aarch64 | replaces upstream's | 786432 | `3b263764ed20482980e3fddd7bfe6e5e3455245ef9cb6f8142dd346b9ea12171` | #29 controllers | Wine, changed by willfaust/wine#3 | ad5e3a5 (2026-09-18) |
| `dxdiagn.dll` | aarch64 | new | 589824 | `4e7fc642b47cd4c36cab6aac55cb9ec947084ef2142489b76505ec670109de62` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `expand.exe` | aarch64 | new | 327680 | `e33d50f1f0996912a8caf29f247196425601e5f46a0bdcd88907258a8e4cdba9` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `fusion.dll` | aarch64 | new | 524288 | `04ed7a54c7be84df04d4911ed8593135a1a3fd25c8c07f05b564144ff67e24a7` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `gameux.dll` | aarch64 | new | 655360 | `47bae7f0dae41494442055652a12829df968d0615e6441937ff0c4015e36d047` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `gdiplus.dll` | aarch64 | new | 1048576 | `0200c701960108420e117f2e31e23802a5b9c4686676b9c9803c61248eebf603` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `glu32.dll` | aarch64 | new | 524288 | `582faef68650996197e371b8a42b3c5b9c658c9b62f48463f9ff63280d034458` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `kernelbase.dll` | aarch64 | replaces upstream's | 1900544 | `18d472c96435acdcaaf0ed288760e4bf0f5a6b83b336dc12b824bdaf1ea18754` | #35 Steam | Wine, changed by willfaust/wine#5 | 4466fb6 (2026-09-23) |
| `mofcomp.exe` | aarch64 | new | 458752 | `7b7999e826147b4b07ae9c53228b2db3ca0b8966d506e85dcefe9f40b69744f5` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `mscoree.dll` | aarch64 | new | 786432 | `f2e9a164b0091b57da18a450bfaa57b55b05fae2853a8be3e8f410f0e632f7e8` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `msdmo.dll` | aarch64 | replaces upstream's | 589824 | `535ff666170bebf34dc36173bff6e9084bba1ed7a7d419b046292a156e3cab32` | #33 media | stock Wine module | cfc6c90 (2026-09-16) |
| `msvcp100.dll` | aarch64 | new | 1441792 | `3d83a7f53fd0a15ff8239de2f3cd5b3d38a78eaa4b272c4120f795b4b9d6a2f8` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `msvcp110.dll` | aarch64 | new | 1441792 | `23be814cab1c2a5e1f329a45fa4c3802f265621d68b721fb8f9e8f9445b59ec3` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `msvcp120.dll` | aarch64 | new | 1441792 | `904e8a23a295c3a43ac9904316a48c1fdf2055302778df3a4fa9dd6e2d0bb648` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `msvcp140.dll` | aarch64 | replaces upstream's | 1507328 | `d28d70d871d6ea55831b07f5fda65e8ce11c98ef6ecdab9ea02b8148f69a805c` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | e88266d (2026-09-19) |
| `msvcp140_1.dll` | aarch64 | replaces upstream's | 458752 | `6490ec5a2c1ccf33b0af0df2286cc1d526da7f04206d35d19aae87bc825b19f5` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | e88266d (2026-09-19) |
| `msvcp140_2.dll` | aarch64 | replaces upstream's | 524288 | `f37888c5d24e03533d78c55af02f2b39b2afb107170bd921bfc4c93c9795d10c` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | e88266d (2026-09-19) |
| `msvcr100.dll` | aarch64 | new | 1376256 | `914dd477ba41a980007c8adc86cedb12dfa60350ce6ac2127932ee17b3506392` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `msvcr110.dll` | aarch64 | new | 1310720 | `01ca54e9a5b265769c9f51e7f22871de0719a020f1014314437f02222de3f751` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `msvcr120.dll` | aarch64 | replaces upstream's | 1507328 | `fef3e13df37f6e496479e1147522ba897c9de0778516c5b0608b33f60b64df5b` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | cfc6c90 (2026-09-16) |
| `msvfw32.dll` | aarch64 | new | 524288 | `cd85b87af6f1690bbcd4a97dd544c0ba1676f79a80ec6d52d423feb5732b1517` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `msxml6.dll` | aarch64 | new | 589824 | `e8af89b308c2570176b3544e54924109a257463b74cc89239fdae6233faaa583` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `normaliz.dll` | aarch64 | new | 131072 | `085aa10e1665d1a8717f4e5203cb589837bd68a150bd589b1b26e88e64b961de` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `quartz.dll` | aarch64 | new | 1179648 | `302ca95f8a7e212f5ceea943a9aa5e70519428ae4e43511ec59af7406825b5be` | #33 media | stock Wine module | e88266d (2026-09-19) |
| `reg.exe` | aarch64 | new | 524288 | `00aa0f00adc4e994bbfa3c68a538ddc114b2b3d849c729074b766fd64a9de14f` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `riched20.dll` | aarch64 | new | 1048576 | `567d057dde4e6147fae10a4242e3e6279790ad9bef388fbfe9e74db82aa60c36` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `sxs.dll` | aarch64 | new | 458752 | `4d626f026e8d3001c4eafcdf90afe3b407024207b072ac5aa1979f9f17e4cd3a` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `ucrtbase.dll` | aarch64 | replaces upstream's | 1507328 | `b36f95228c415dfd62a0ed13b757da4c70bf225d56c8ecdf06075e599430d406` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | e88266d (2026-09-19) |
| `usp10.dll` | aarch64 | new | 131072 | `eb633038b647f2930ddcd659a4e15574af3fb915f47518495e48a63f18b4a5db` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `vcruntime140.dll` | aarch64 | replaces upstream's | 458752 | `85bc05e86ba327075ed3e57ab838a1cd5ec7ed2829310ac9c26ce11a0221b84b` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | e88266d (2026-09-19) |
| `wbemdisp.dll` | aarch64 | new | 524288 | `a895dbef35b2d1ebf33612d56b5a2d3f13383bb0de2f9eadfcce38b79390f32c` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `wbemprox.dll` | aarch64 | new | 720896 | `11cea2bdbddb076c6df948ae37efe6c155eaafce8d83af9ac8088b8f059a975c` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `winegstreamer.dll` | aarch64 | new | 983040 | `5ead49a7afe3ee2e14113a8f0f441a849a8496a169658da86933baee6cd6af12` | #33 media | stock Wine PE module; its unix side is #33's | f254fcf (2026-09-18) |
| `winspool.drv` | aarch64 | new | 589824 | `cd11e11d44efde18d78dc5a63fad143921f2d163adb1e429f5e38c78fbe096f5` | none (64-bit farm breadth) | stock Wine module | 68ccd70 (2026-09-14) |
| `wintypes.dll` | aarch64 | new | 589824 | `b928111bd1ac94b9b02d0fdd6739931d158d779bf0b5d524c1c47b005cf10594` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `wmadmod.dll` | aarch64 | new | 720896 | `ce2ef8921bc0946f007aa89293cc1774607087751c10cdf950bc4bb89bbdfe09` | #33 media | stock Wine module | f254fcf (2026-09-18) |
| `wmic.exe` | aarch64 | new | 524288 | `8f7203bbd2c8b34b52320940d08edaa5d76b246fd3cbee1d92e8196bc3dbf3ec` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `wmiutils.dll` | aarch64 | new | 524288 | `6a7983031d0cfd4794e672be9e316a7c6e2726488816c3e741c85420f611442c` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `x3daudio1_0.dll` | aarch64 | new | 458752 | `bf16cdb22616fdc0c87750681aa78e36de8761d2536a8cfe6e117625e0929fd7` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `x3daudio1_1.dll` | aarch64 | new | 458752 | `37ee94c1b045315a2cf949368f65b6bbfa1dd9ad958705a3fa8a0ad311e2548b` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `x3daudio1_2.dll` | aarch64 | new | 458752 | `e078f47f76dbde105f3e1bf1a7d89ab5205eab3994c3905aa3b390a97b56d7bd` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `x3daudio1_3.dll` | aarch64 | new | 458752 | `f56bc29b18b0669e88c7337eac559b802295da10bcb293b0fc256611ac8d670e` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `x3daudio1_4.dll` | aarch64 | new | 458752 | `fd417a223af28e4c8cc417a7b2fd92dfd065eb60a5e141d300033d601018ab54` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `x3daudio1_5.dll` | aarch64 | new | 458752 | `3d8f880bfe5103264bd8605a3367f0c8fabed6c1556020982926f7a6898fcfc1` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `x3daudio1_6.dll` | aarch64 | new | 458752 | `3156fba595babf0a1921e502f71ee7fecb9644aba2384eeae31f4ff79d1d6eee` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `x3daudio1_7.dll` | aarch64 | new | 458752 | `341d5b9642415ba2d9a91c31ca2f957b8394164a2040e876c59c02ff29c5f750` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine2_0.dll` | aarch64 | new | 917504 | `4eaefea10395940376dcafe161f4efb102cf8838bd5c9d9701df1d072d460156` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine2_4.dll` | aarch64 | new | 917504 | `4521cd41f9bc632c587478989299354fc77366cccfb571268a69eab86a13dba3` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine2_7.dll` | aarch64 | new | 917504 | `1e2ce89158c4b620eb66118a13086370ca2c7c429d8f8b382fae876b9ea35400` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine2_9.dll` | aarch64 | new | 917504 | `7ed49a0241bf3196a11e73b02dbf7babd0e4ad7c78a4972cd19502edee2b4c10` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine3_0.dll` | aarch64 | new | 917504 | `b6bae10e488d5754042eb36a7acabe1bf7c9d8022ef6789bbea5b2a861a9d0f8` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine3_1.dll` | aarch64 | new | 917504 | `91309e0acc2426a6dbbb884d0ad6437a640f197668bebc970e25bf5138698ff3` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine3_2.dll` | aarch64 | new | 917504 | `0d8a511734aad81fdc177e25f63b70cdecafc8af31da9d30dd8632845f274227` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine3_3.dll` | aarch64 | new | 917504 | `04fbab6be24ce7e7bdb0f6ae460271ba44ef6e4e98efa02ea306215a9c5a5475` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine3_4.dll` | aarch64 | new | 917504 | `a92cd86556dec83a4f2393b4702c43815f432f694ff3039e0e5e280a16ae35c5` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine3_5.dll` | aarch64 | new | 917504 | `70d67b8a0888fa5b27fc899e99cea731114e60998bd96c26eeb6bcd615e46278` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine3_6.dll` | aarch64 | new | 917504 | `6e360491c92ebdc607a37f378bdbd797d0078ac6b04a26b62e6db7ee3404fe3e` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine3_7.dll` | aarch64 | new | 917504 | `4c73f001d8125272c1092efb7cbaf3597e3ee0ab1b5ce4e9f00d51a2a6fe5d9e` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xapofx1_1.dll` | aarch64 | new | 524288 | `c8d629b3498ef530fb1b40b24e5dce7a03bbcf5f9f415908255790cba73ae532` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xapofx1_2.dll` | aarch64 | new | 458752 | `9206215e41f0e31f4c5dfe4b7fda05af3a46fe3e4d8e9b19f2f1444b15fe139b` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xapofx1_3.dll` | aarch64 | new | 524288 | `4ff2d6c751b3f54a9b09a3b55e7f292127f2029cc71ccf66e47a068822b6a587` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xapofx1_4.dll` | aarch64 | new | 458752 | `6d923a15fd2f0bcf811c3b4eaee419738912feed2b7b4ddf2ca4f5a8a6cddbad` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xapofx1_5.dll` | aarch64 | new | 458752 | `a4144bc5a23fc926a7104dfe8abd12c19fcd175c07bddf8a9aa184b0b1d59310` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_0.dll` | aarch64 | new | 851968 | `b02e6260288403f5919cc4b1067393712beac299e0c656b6cd05d4e87fef7780` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_1.dll` | aarch64 | new | 851968 | `7969dc5c02aa58452789eec26828b161cc2d58e35beb7e973dd132dc58c3807e` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_2.dll` | aarch64 | new | 851968 | `dcf9f8d2bf65d270aee85392c0d5de475002fd7772662067d34d50ca60672177` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_3.dll` | aarch64 | new | 851968 | `8ebb4169fda1c2ecb527df6ec92183019b2372160ef25ce322c8d68010654e81` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_4.dll` | aarch64 | new | 851968 | `6b33d8536a47d3c74ffe85d5598a9167c7758138f28959f823bdc620aa81636c` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_5.dll` | aarch64 | new | 851968 | `8778963f2fb3898839ef656d11f3e752dc1ac760b050c2b360fd4ebda0c057cf` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_6.dll` | aarch64 | new | 851968 | `5d850f2e7ded95f9f17ae14c66086c9e0de34eefae767ac913feca3defbf1f23` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_7.dll` | aarch64 | new | 851968 | `306ffab1b240ed2bb6d050488337bc479a806b4eab94f724cca6d45581e45454` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_8.dll` | aarch64 | new | 786432 | `f8b0dda6c3d9bbb6f7057e7e6b6ad9504bc78ff7c1a0b526bfbd97dc266f480b` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_9.dll` | aarch64 | new | 851968 | `d9adc807cffce378349d8e3d7a22e2b0076458fa7875da0214803a5cc4fc11af` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xinput1_1.dll` | aarch64 | new | 524288 | `b8bf17ddf8426f4f81bc667f854f2dde6644e7568def74c034eefdb7c2eb5691` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `xinput1_2.dll` | aarch64 | new | 524288 | `d65f8716e0d8322b8d46812227c24662cade7fd35955681a4848a5b80a062d2a` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `xinput1_3.dll` | aarch64 | new | 524288 | `a31a6bc4abf4d35286d952fbbaac536fa8b2dfe6db77626cd7c662ab19ed917d` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `xinput1_4.dll` | aarch64 | new | 524288 | `549f12ef5062a85ae8566ea9ca28d0de9e6675c8f4704e1d01aa0430741366f9` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `xinput9_1_0.dll` | aarch64 | new | 524288 | `9e82b046888c0244d1599ebc38427ca6db4438b30be7263dc1480a191fe62927` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `xinputuap.dll` | aarch64 | new | 524288 | `6f9d200d7e085f9f6695bd25a9fe2c1ba9f30f946ed3c13915a9d774703235c9` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `xmllite.dll` | aarch64 | new | 524288 | `c92ccc8a3030fd51d2f36f46602b0b90063bf924e50ebd59f4e091eea33dc936` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `avicap32.dll` | arm64ec | new | 589824 | `6a3e70e719c7e488c9191af22b46f084f53ffa7ae690d93d9e708528995e1dfb` | none (64-bit farm breadth) | stock Wine module | 8ea6ec1 (2026-09-19) |
| `bluetoothapis.dll` | arm64ec | new | 655360 | `06669f7108252af84f8d110955aeb7072d4e8e197870510c5451b1e5cf045de8` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `comctl32_v6.dll` | arm64ec | new | 2097152 | `c75b4f0284301b4d86cebf011ea34129557231d27cfe46a319ad9e43e29ab75e` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `concrt140.dll` | arm64ec | replaces upstream's | 655360 | `d749a77283e5e5531041c648be10a15a38ea33c86da2d5a637badffb5f261ef4` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | e88266d (2026-09-19) |
| `d2d1.dll` | arm64ec | new | 1441792 | `eff82f9f55ad538fcfc99599cb42ef63c6ea2abebf0ec7223a80f0349bace72e` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3d10.dll` | arm64ec | new | 983040 | `3333fe2eb618c11965dbed3bed632f57b7335f0c6f3af45572186747f7f038e0` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3d10_1.dll` | arm64ec | new | 655360 | `5680c357b929180e9bc395cb721335a52bf63a425319e96518126d4ac9c3f9bf` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3d12.dll` | arm64ec | replaces upstream's | 411648 | `59514853d283732e50ad4d5bde761ac273e2826b7473a5b35657c847f547340c` | #32 D3D12 | Madeira D3D12 runtime (`research/madeira-d3d12`), changed by #32 | 7a606ae (2026-09-25) |
| `d3dcompiler_33.dll` | arm64ec | new | 851968 | `e2c8f085ccd61382bada0c02c772133c0ecc12d29074d991795b8b1589c799a0` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_34.dll` | arm64ec | new | 851968 | `df9365f3c00c8cb6fdccd616eb9db0bf6fea0d40e6b6f82bffcc6db3657742c1` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_35.dll` | arm64ec | new | 851968 | `82c768c7c2dade217a25df26aa9ec1b8066bcd327f1ef9a16a933023d2b074c1` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_36.dll` | arm64ec | new | 851968 | `9e22c0cc5bdc04356b1aeb95b528606f940b9cd7dc20765bd8037d9a310c9699` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_37.dll` | arm64ec | new | 851968 | `1db5d86f46ca80a5cbdf6d1aa0329f7c114f8353276d3e175e1d80755244b03f` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_38.dll` | arm64ec | new | 851968 | `abd477d7832b0476a9550f0b1c6ce736527834ad61067bcc7ba14d338c88a5d3` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_39.dll` | arm64ec | new | 851968 | `0ce8685b5430e68618bd03530bd94cd27dac0d4de5b9fadf8a3a81aad4ef89b6` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_40.dll` | arm64ec | new | 851968 | `47a7816ec78d27c503315e074a08f33ab650d195c0cbf1d896b7ef2b91625a4d` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_41.dll` | arm64ec | new | 851968 | `12ea4c30d416ebf1e8112ff1b8a102b4b0d792a760775796e64411e24aa74fd3` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_42.dll` | arm64ec | new | 851968 | `4c2d20c0f55723232c853a61b81898700f47f1f45320e1568b42398705e8f704` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_43.dll` | arm64ec | replaces upstream's | 851968 | `31dff9682f1862ed16a67199bf11fe4931d9e0c1e74c668ab7b6ebea1d28f47f` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | e88266d (2026-09-19) |
| `d3dcompiler_46.dll` | arm64ec | new | 851968 | `8a2940cda42948773f3d9c228521df272a6dca7f62000b4fdc2e133632ebeeee` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dcompiler_47.dll` | arm64ec | replaces upstream's | 851968 | `0459c76fa3e0f632722897ceb9c092689c76c000dd29711372ca23efed90c178` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | e88266d (2026-09-19) |
| `d3dx10_33.dll` | arm64ec | new | 655360 | `55a9794ee86fc0955e9d66eb350774768346934d32d6873ea001715bb0882cbd` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_34.dll` | arm64ec | new | 655360 | `0cf42f389076e5d78230779cdb334ff4727430c6cc29d94fbfb43ad6e19af8d9` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_35.dll` | arm64ec | new | 655360 | `dc937c737f3bf75d75b426f5c1d035644eed534b2be86256e44ffaf850b40754` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_36.dll` | arm64ec | new | 655360 | `66c9854cc2f56515a8166ba26751f6bf9f7dc96dd93d3cf5b867383344595020` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_37.dll` | arm64ec | new | 655360 | `281302e18547b779923571fb2df4a19b84b8082c85d41804d8be50355614fbae` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_38.dll` | arm64ec | new | 655360 | `69fadc5bee96ca8a9e1fd20a2a70a4c06ddf79509adb87174c86f6027df69844` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_39.dll` | arm64ec | new | 655360 | `d7822e2788e15f92742627cfcfb4ba211095a20f4eb70138e81e6b703fc16d1c` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_40.dll` | arm64ec | new | 655360 | `f0bdd5e664aacfe126e852da5a2d194a1ee04d3b016c4084f784608dad13687d` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_41.dll` | arm64ec | new | 655360 | `e43e64fe72c2e87281f5015deeaa164fedb2baac2132c026c98f1527215a8a7f` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_42.dll` | arm64ec | new | 655360 | `23f47599c64115ebc74f3e45380b30f211b6b38455e146f8ebf1cb1ffe08ba00` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx10_43.dll` | arm64ec | new | 917504 | `30bafcb46adc851fd92960ff46193c32826fac0f57226d10f0e927749ae32569` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx11_42.dll` | arm64ec | new | 655360 | `9368b87f8f0f9ba4965c8286d47fc50f8bda8deebef315c43b577ac582daab8d` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx11_43.dll` | arm64ec | new | 720896 | `b196d50833514fce66919de06caf7a5f49a9a763fd62a4f825710f7ff888685f` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_24.dll` | arm64ec | new | 1441792 | `9bcec66fd0c555d23cdbbbc45337a620af2d9a7c091bb68637dc608cc82205c0` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_25.dll` | arm64ec | new | 1441792 | `a20bdc2c811e0b8908ff35e768d8e9282f00982c764611d1a7e07e5eb12c6091` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_26.dll` | arm64ec | new | 1441792 | `6e4b18fe773e610ff45187f0b0ea16823515776801c7317bae53183e9eb0efe3` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_27.dll` | arm64ec | new | 1441792 | `6039fbfd067679a60a161ae98110374076ca8adcb207f444c93878b2311f447c` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_28.dll` | arm64ec | new | 1441792 | `4449408ae22ed88c44d1a0f7e4f125431e7bddc45294886b12845e6c796bf534` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_29.dll` | arm64ec | new | 1441792 | `9f9d0d76b535a50542c181ee50c9c6b33eb7afd07732ce5eaefadb36d86a61af` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_30.dll` | arm64ec | new | 1441792 | `2c644eeb3f06d0ba3282e369857a3aaa0ea2039b96bf4272b155f03ad92cf7be` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_31.dll` | arm64ec | new | 1441792 | `391f25a53953cd91270574970a0f2397ef60610dcff606f64441750dbc6bd73e` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_32.dll` | arm64ec | new | 1441792 | `e189056a7390596bd4f7823e22604ccf521dce25e367daabeb25cea159167eae` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_33.dll` | arm64ec | new | 1441792 | `c6e91b38e077d0814772441b3dc40cd074856cf36cd697d91b943f83d612c653` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_34.dll` | arm64ec | new | 1441792 | `944f22899abfff808595f055323c939e5c5aa0152c79b88771ecaf165ec6a7d0` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_35.dll` | arm64ec | new | 1441792 | `784914ef40bba250c0ce2bcaf9d8b3656d59d0d2e62237a3bbdc6170e4b4706a` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_36.dll` | arm64ec | new | 1441792 | `8da962973e9b4ab369e79532b4ff6f2366621cdacedf1d81fc904a54ea3c4718` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_37.dll` | arm64ec | new | 1441792 | `325bd453b74a0ea47b297808c498f185baf7faa9083b9368f9796c199a2a4588` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_38.dll` | arm64ec | new | 1441792 | `df5fc278821df6c885c24f3ecb530a85045c0d70c0ddf809565424c289156277` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_39.dll` | arm64ec | new | 1441792 | `4131f1cb55097100ea0060ea4a842255ac7019fa86353d5b8e607129b2078642` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_40.dll` | arm64ec | new | 1441792 | `e41dbecbbf3f6b4870b81e9724f58ab95cfa4f043f41edbfe4f3a0b6e69314ee` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_41.dll` | arm64ec | new | 1441792 | `f725f21e74b8eccf7476d795dbae6ddca6b35c0b57a06a3a1681e2a14c380956` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_42.dll` | arm64ec | new | 1441792 | `fe617f2cd86833cb2104489ed23d5a4021adea9c863f3a2ee62171992177cf38` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `d3dx9_43.dll` | arm64ec | replaces upstream's | 1441792 | `b77f57e89b435a9e5725b5571404103842df0bd6cabd3094b85faf635e5d41c5` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | cfc6c90 (2026-09-16) |
| `d3dxof.dll` | arm64ec | replaces upstream's | 851968 | `84ce9325447786f57f5d74f64ac67fe1e53c4a888e5e3f6e365b584c83cf6671` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | cfc6c90 (2026-09-16) |
| `dcomp.dll` | arm64ec | new | 655360 | `eb3cd0f12e48026f9f98ac90c069353fe617841b6edf545ac7fa41d4ecc72eaf` | #32 D3D12 | stock Wine module (#32 asks for it) | 7a606ae (2026-09-25) |
| `ddraw.dll` | arm64ec | new | 1310720 | `ef0b01e65b8dea278645860a4be82e7022cbe4f06fd7cc2e6d09abbe019db27e` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `devenum.dll` | arm64ec | new | 851968 | `328e9e06561768090ddf8c88b4729865aa858d8fee3e0b321f8d3f7cb83c98fb` | #33 media | stock Wine module | 8ea6ec1 (2026-09-19) |
| `dinput.dll` | arm64ec | new | 983040 | `da9065c3f4ef5857ef5672ba285a9d6da7d2444fbbd5ca3c2c02c2239f5b496f` | #29 controllers | Wine, changed by willfaust/wine#3 | ad5e3a5 (2026-09-18) |
| `dinput8.dll` | arm64ec | replaces upstream's | 983040 | `a892f29e7ab9303c8e8d8d8731f6d56af6927b0c099a43e304d6f8f560bcd18b` | #29 controllers | Wine, changed by willfaust/wine#3 | ad5e3a5 (2026-09-18) |
| `dsdmo.dll` | arm64ec | new | 851968 | `8468006142874a02a1944135f258c11e218c3fae546270b75efb9b4dc23aeafc` | #33 media | stock Wine module | 8ea6ec1 (2026-09-19) |
| `dxdiagn.dll` | arm64ec | new | 720896 | `23f84ff2374dc0b4af0a5b390b72967e7d76e5aedd2050ed1d69cb00135405d8` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `fusion.dll` | arm64ec | new | 655360 | `4909d5bca17ba5c094def79757fe6d2da6fb35b8c50702c1115d36b877be9a25` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `gameux.dll` | arm64ec | new | 851968 | `c080eea35775df3ab3d5a93a0f2242a29754db8cdcf087c28ccbd0ebc747ae4a` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `gdiplus.dll` | arm64ec | new | 1179648 | `c74aa2fb6fff4ac1ee211613b607d8eff6b8cf0eb11a03fa1fc8d965b9e8d6c6` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `glu32.dll` | arm64ec | new | 655360 | `ba180c4b34f2d19a3bbdd108afa7499510abed2d38386f9325b8257a8330763c` | none (64-bit farm breadth) | stock Wine module | e88266d (2026-09-19) |
| `kernelbase.dll` | arm64ec | replaces upstream's | 1966080 | `fb614b15545b7ddeac30f17aa7421210dfe94661418193d017ec6a39cc7bdd9b` | #35 Steam | Wine, changed by willfaust/wine#5 | 4466fb6 (2026-09-23) |
| `ktmw32.dll` | arm64ec | new | 589824 | `5b1c1f7bc635274a605a953cace44122367d32f5998bc77652fc9980c8eecb4e` | #32 D3D12 | stock Wine module (#32 asks for it) | 7a606ae (2026-09-25) |
| `madeira_d3d12.dll` | arm64ec | replaces upstream's | 411648 | `59514853d283732e50ad4d5bde761ac273e2826b7473a5b35657c847f547340c` | #32 D3D12 | Madeira D3D12 runtime (`research/madeira-d3d12`), changed by #32 | 7a606ae (2026-09-25) |
| `mf.dll` | arm64ec | replaces upstream's | 1245184 | `a87f053c3add85cba8fec52e1b5a4a5056c6223fd4972f0c2befa7a0933de466` | #33 media | stock Wine module | 8ea6ec1 (2026-09-19) |
| `mfmediaengine.dll` | arm64ec | new | 917504 | `a7319f019df771532f93a95322b9d7654f38fac6a6f8ccb5bd07fb23baced3a8` | #33 media | stock Wine module | 8ea6ec1 (2026-09-19) |
| `mfreadwrite.dll` | arm64ec | replaces upstream's | 851968 | `018669bb36180fa45dc0c68dee44e18390cba1075e29a9af0664925dd2d345bb` | #33 media | stock Wine module | 8ea6ec1 (2026-09-19) |
| `mscoree.dll` | arm64ec | replaces upstream's | 917504 | `1d19979b536b8b348d90ae88adce86d60279d6004ae47bec772eca1d9ca686d6` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | cfc6c90 (2026-09-16) |
| `msdmo.dll` | arm64ec | replaces upstream's | 786432 | `8035bf28c4efeb34b4fb40dafc2ea96eef7c6a7fcb338f6b6537ca9bc20ce15a` | #33 media | stock Wine module | 8ea6ec1 (2026-09-19) |
| `msvcp100.dll` | arm64ec | new | 1507328 | `094c203be2249e6b56ce99aae45601bef838621c5a9f54179984c929787d262c` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `msvcp110.dll` | arm64ec | new | 1572864 | `e8ac5bb2e27183d5cedb1de5ed3424efbaa32f94f292722fb364729ffbc3d205` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `msvcp120.dll` | arm64ec | new | 1572864 | `1918e61c5eae1fb2f7861bb4214dadb01645871bba424d2dee2f383de9055174` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `msvcp140.dll` | arm64ec | replaces upstream's | 1638400 | `78cfa6c424118d5325df97b3a9e424d8c8f2991377b82f33cc9a75dedab078fe` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | e88266d (2026-09-19) |
| `msvcp140_1.dll` | arm64ec | replaces upstream's | 589824 | `5864e9c0df44562162722faf0c0891b3fd0974c3edb7e0d6b497428f61f0cd6b` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | e88266d (2026-09-19) |
| `msvcp140_2.dll` | arm64ec | replaces upstream's | 655360 | `d193fb163d0f389f0f11cd60c4f85e1993f6578fdbc9f8dd1dceb1fe1e44cde7` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | e88266d (2026-09-19) |
| `msvcr100.dll` | arm64ec | new | 1441792 | `c3ebf5cbd5da6d319314bdc8d73500cb50aeb3df0b45bde0fa1d9991b95a0af9` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `msvcr110.dll` | arm64ec | new | 1376256 | `5acab589815ac83d7eeb8ab3dce289184ff0aa19a668ceaf4a1a96462f49f47c` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `msvcr120.dll` | arm64ec | replaces upstream's | 1507328 | `86d026966fdadac42caff5ddbe5d746e3a0e4c72f72eb4afc9bdde475b37dfe5` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | cfc6c90 (2026-09-16) |
| `msvfw32.dll` | arm64ec | new | 655360 | `b26d8dd15a4e801da8aa938545fceed88024e4620172b5c3aab02e301c7b79ec` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `msxml6.dll` | arm64ec | new | 720896 | `83e7671ab69797168c5768120a6d882fce4341f0ba1d722a86783503aaa4bd13` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `Normaliz.dll` | arm64ec | replaces upstream's | 131072 | `8ba48d221044b9149b36670ad9e209aa123be89474cad947adec5ea30c6997a3` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | cfc6c90 (2026-09-16) |
| `qasf.dll` | arm64ec | new | 983040 | `5c8f6fb4b3b1e0e36ffdbc5efcbd03e1440380ebbeba2ac3883bc0aee3566c2d` | #33 media | stock Wine module | 8ea6ec1 (2026-09-19) |
| `quartz.dll` | arm64ec | new | 1441792 | `a201716add14dbaf806e66c9f5f6df70d9732b10e2d9632f8e14cdb07c524ce6` | #33 media | stock Wine module | e88266d (2026-09-19) |
| `riched20.dll` | arm64ec | new | 1179648 | `c4fb926b205d89446b9ac9fe430da2e1b12cbf6a0f3308f614876dce6285738c` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `sxs.dll` | arm64ec | new | 589824 | `547464c6497da059a40dafe3da6881e77f434a355255ea70507a8feab109c350` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `ucrtbase.dll` | arm64ec | replaces upstream's | 1507328 | `7a49eb70985e0684848a40cd03679c43b9ec9eb83540132a63061599034f26a4` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | e88266d (2026-09-19) |
| `usp10.dll` | arm64ec | new | 131072 | `ea85fd2f56dfea58ad39f37a37e7e3103178a5be7e9cc021e7114c5f0418c084` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `vcruntime140.dll` | arm64ec | replaces upstream's | 589824 | `7a90f85336896359a2ec5639c67b1c6c24e3536f1711b6eaf6c1d2bc6aeb65a6` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | e88266d (2026-09-19) |
| `vcruntime140_1.dll` | arm64ec | replaces upstream's | 655360 | `48f76c813d48c09bad90301fe25a9ae95090d74820dd816b95b6066a5ec2237c` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | e88266d (2026-09-19) |
| `wbemdisp.dll` | arm64ec | new | 655360 | `0391f32661726666e4e65c650f15ff999bf4a6c878c8add01db2861d4767d5f6` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `wbemprox.dll` | arm64ec | new | 983040 | `4cb01626cd2e8ac01768e5d947bf6be4ae9cb1caa394ad37967745c98f1f2c3a` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `winegstreamer.dll` | arm64ec | new | 1310720 | `c6aeedee6863183fa40d2a29e8f7fdcf908c9027ccdd00cdac90be7a286230c6` | #33 media | stock Wine PE module; its unix side is #33's | 8ea6ec1 (2026-09-19) |
| `wintypes.dll` | arm64ec | new | 786432 | `bdb1ffee1a727f902491040bcfc9657e717f95135ef08186d409d0440149571b` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `wmadmod.dll` | arm64ec | new | 851968 | `d705e6fd4839f3baeca7491257e077d2f7352e8c48affc33876e4fad69d630ee` | #33 media | stock Wine module | 8ea6ec1 (2026-09-19) |
| `wmiutils.dll` | arm64ec | new | 655360 | `4801df69bb091c90b8b74cebbe7a8d4c01338aa05021686b76466034e31a8211` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `wmvcore.dll` | arm64ec | new | 720896 | `b693813e7f3fa0687e0460725bae1264c8874f4b00f060be62c88bf9d7db6ad2` | #33 media | stock Wine module | 8ea6ec1 (2026-09-19) |
| `x3daudio1_0.dll` | arm64ec | new | 589824 | `56dd906c6afef8b99840b663e07b072c9da262c1186cf40ed6f915ee87ea8c05` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `x3daudio1_1.dll` | arm64ec | new | 589824 | `3fb4686eb802830a57084e5ab5011fa0ecd1ebf8d6e2ed70d7fc51aa980f8f24` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `x3daudio1_2.dll` | arm64ec | new | 589824 | `0abcc6daa8c6f53a56d46de8c9a20d2065d3dc1e87a341aba72b066c300c4a83` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `x3daudio1_3.dll` | arm64ec | new | 589824 | `5b090feb61520ddcd5dc4e71877511ffdd229665b697153fa1341b9a23dbd3c7` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `x3daudio1_4.dll` | arm64ec | new | 589824 | `ce44e33681061bd73b2e258894282517bca09e5866bc27266635a1a621cbb094` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `x3daudio1_5.dll` | arm64ec | new | 589824 | `fb4a31c0d0f2da08a61d58ad1155fe9a47aefc601a80e0823832137a61d57bed` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `x3daudio1_6.dll` | arm64ec | new | 589824 | `21768cb298c927d169bd16aae23fd1f9a507720034c6be3a4b2f9393083bf0e2` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `X3DAudio1_7.dll` | arm64ec | replaces upstream's | 589824 | `c81a7cbf0ec46d847d0591c56b9a3c7557cd1e8bb4acbadf72d1f1c9e2f5bacd` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine2_0.dll` | arm64ec | new | 1048576 | `ec405eb3e4fc76ca2e2cd79551ca98b42206a5401d3849ba5302eef2777a93f7` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine2_4.dll` | arm64ec | new | 1048576 | `c4a485c5e91e0b6d058893732dfbe5ff6cbdce386a2540d5c38033e5b265c93a` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine2_7.dll` | arm64ec | new | 1048576 | `2e5bebbde51e59efb81f87f4ca52c764746a196acbedbe7c999246019162a2b6` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine2_9.dll` | arm64ec | new | 1048576 | `bd59749984ad68d5b35ac9340814e96f73ca1b028a577fc2850f1f9535e45f66` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine3_0.dll` | arm64ec | new | 1048576 | `d81e8fb5bfec371bddcf0c08f7be7c1f7403a75e9413eb83278a246d6f587420` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine3_1.dll` | arm64ec | new | 1048576 | `79d4d2fc4cfcf5a5442b6e9d662901c3ac45e8e8a7978ecd186590e56bed58fe` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine3_2.dll` | arm64ec | new | 1048576 | `b2ee05b320f0cc99f9512447537030e047e7eceb5329da4071f31cdd9d1c913e` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine3_3.dll` | arm64ec | new | 1048576 | `1589f76a11b3cc1594c7bbc3ec2857b306eec7a0cf4710400b9049c1ff79c2ce` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine3_4.dll` | arm64ec | new | 1048576 | `6d65d7bedf58940c1e85aa4a487fdf65353f8e035032120f690c6dbba76b8143` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine3_5.dll` | arm64ec | new | 1048576 | `73de94f91c17af000710ecf7887b5db19fb088d940da61047f4acdb6b447a3ab` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine3_6.dll` | arm64ec | new | 1048576 | `55e64c96db875a5bf0ebfaa3107a66aadafcc0788f5c8f19f76afe06e4e899e8` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xactengine3_7.dll` | arm64ec | new | 1048576 | `5292f7b1ba2a287ab23f720ea74a1e328c26bc29380220ae0b5bb920aecaf8ca` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xapofx1_1.dll` | arm64ec | new | 655360 | `c8986b57ed7e1e85ea70186e1d310eab83305a6416c6e816efee29e007b692e9` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xapofx1_2.dll` | arm64ec | new | 589824 | `6ed2801ee6e608b6892a474ce2356f6f67a7ca963d0961fd7569292651ec713d` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xapofx1_3.dll` | arm64ec | new | 655360 | `b29d81ed6ebc6c22073dbb2ed9198367daa481dcb031c66ddd78f3fd1bd6cf5c` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xapofx1_4.dll` | arm64ec | new | 589824 | `0fe693ff53dabd71ddf4b85c93e42eb7758694b004fb9548dd24866652075c16` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `XAPOFX1_5.dll` | arm64ec | replaces upstream's | 589824 | `10e10cc24b5d438ca5c786ac3c4fa0fe6fba057777ee98fb4fdc2b481a6ce721` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_0.dll` | arm64ec | new | 1048576 | `a6878146af254244e04afca6e2852d557af184fe925fc4c305e66393197ef529` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_1.dll` | arm64ec | new | 1048576 | `12df154b3ab5db0f96c31ab381896c35f81f54e076d0ccaf63626dea3c65b480` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_2.dll` | arm64ec | new | 1048576 | `8c5b18372624223174d83e0241931e6da5556ba7d7ba1262a93ef64d9e477858` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_3.dll` | arm64ec | new | 1048576 | `06ded367832fc1f1a19670a4bfea69be97e2f2164ceff544fec0ff551abd5ca8` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_4.dll` | arm64ec | new | 1048576 | `c142aef8d4286ff852e9860e2bbecc79c6c9b3a0fbeb8e53d9c2a3f8ed3faeb7` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_5.dll` | arm64ec | new | 1048576 | `918d63d40f54be95ad9111d6f305e00c91a535ffd9812d4cddd3670089503df5` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_6.dll` | arm64ec | new | 1048576 | `8a3826255d183de5aecf3c99dd2a6074d02b98869c1f8a5765eb56baf299bb48` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_7.dll` | arm64ec | new | 1048576 | `e92f6f0f8d0c9a45e4e4765e553f255d9e12a341925e90045f057226a4b91f21` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_8.dll` | arm64ec | new | 983040 | `de1a8bb6d691bdf8e9d88903b213a2c612d3f37c8008efe52ecd40ec49184ba0` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xaudio2_9.dll` | arm64ec | new | 1048576 | `fb48c0bcc9c59a2e3b90185dca27d7282d01a533626ca49b86a5def5b1fc41ff` | #33 media | Wine with FAudio changed by willfaust/wine#2 and #4 | e88266d (2026-09-19) |
| `xinput9_1_0.dll` | arm64ec | replaces upstream's | 655360 | `bc1f66147d12919671395badaaea3ec22dc996463a0563a6a4b7064387a19317` | none (64-bit farm breadth) | stock Wine module, rebuilt (source unchanged) | cfc6c90 (2026-09-16) |
| `xinputuap.dll` | arm64ec | new | 655360 | `7dd59d93d298ac2c0d13a75281c0c3f737e64e9d1f2a45f53dd87f2bccaec788` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `xmllite.dll` | arm64ec | new | 655360 | `20dd3afd60373631bb6c4da03abb3b01c7e1bbb28bd117f381e83e9b8767a15d` | none (64-bit farm breadth) | stock Wine module | cfc6c90 (2026-09-16) |
| `winegstreamer.dll` | i386 | new | 634880 | `d361abce804e13723c1a24b5de01824fdda0af83c53700c077ddb696433b05cf` | #33 media | stock Wine PE module; its unix side is #33's | f254fcf (2026-09-18) |
| `wma-x86.exe` | i386 | new | 163328 | `183273c85697d741789a1e50e567974d7d20a6a0bc03910cd0aa92d0ae6fb26b` | #33 media | test program, source `build/x86-tests/wma-x86.c` in #33 | 3b2e7fa (2026-09-18) |
