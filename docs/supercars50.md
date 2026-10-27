# Supercar batch: 50 additional variants

Reviewed on 2026-10-27 against the 345-car catalogue at commit `62ba54b`.
The resulting catalogue contains 395 cars. This branch builds on the JDM batch
in [PR #1](https://github.com/aqaPayam/supercar-archive/pull/1).

## Scope, duplicate review and evidence

- Entries distinguish body styles, meaningful powertrain revisions and factory track derivatives. A changed year or cosmetic paint scheme alone does not create a new entry.
- The full existing manufacturer/family/variant inventory was reviewed before selection. In particular, the open-top 360, 328, Dino, LaFerrari, Aventador SV, Reventón, Centenario and Sián are distinct from their existing closed-roof records. The 308 QV coupe is distinct from the earlier Vetroresina. The two Super Trofeo records are factory race cars, not similarly named road editions.
- Import validation rejects reused IDs and normalized manufacturer/family/variant identities, even when the generation wording or reference year changes. Semantic aliases still require the documented human/model review; fuzzy names are not assumed to prove identity.
- Every technical attribute and engineering note cites a manufacturer archive, technical release, owner handbook or official retailer publication. The manifest records exact URLs and qualifications. No crowd-sourced specifications or invented production/color totals were added.
- Years identify the model unveiling or historical reference. They are not asserted production intervals; unknown ending years remain null. Announced allocations are labeled separately from confirmed build counts.
- Track-only cars and the unraced original CCGT prototype are explicitly marked as not road legal. Factory track specifications exclude subsequent third-party road conversions.
- New attributes, facts and media use variant scope. Existing family identity/history records continue to inherit through the archive's normal shared-data view; they remain attributed to their original owners and sources.
- Numeric kW values are either published directly or explicitly calculated: 1 PS/CV = 0.73549875 kW; 1 bhp/US hp = 0.745699872 kW. Ambiguous manufacturer `hp` notation is retained without conversion or a misleading kW filter value. Hybrid totals are separate from combustion-engine output. Bounded or missing outputs remain qualified.
- Ferrari 812 Competizione A does not inherit coupe-only weight or acceleration. Nevera R uses labeled 2024 launch claims rather than mixing in later record runs. Gemera uses the 2023 HV8 client specification, not the earlier three-cylinder concept. Hennessey F5 Roadster excludes later Evolution/manual upgrades; its 300 mph ambition is not treated as a measured speed.
- Animated McLaren headline counters and an inconsistent Aventador SV Roadster promotional header are excluded in favor of full technical tables. Dry and kerb weights remain distinguished.
- Each entry has one licensed representative exterior photograph, visually checked for the intended body/model. The selected Commons file page, creator, license URL and downloaded-file SHA-256 are retained. Photographs do not certify exact engine, market, year or equipment; the Gemera caption specifically notes this limitation. No manufacturer marketing image is assumed freely licensed.
- Prices, color availability, geographic distribution and unverified performance data remain unfilled. No website behavior or source layout was changed.

## Additions

| Manufacturer | Variants |
| --- | ---: |
| Ferrari | 19 |
| Lamborghini | 12 |
| McLaren | 8 |
| Pagani | 4 |
| Koenigsegg | 3 |
| Hennessey | 1 |
| Rimac | 2 |
| Saleen | 1 |

| ID | Reference year | Variant | Road use | Manufacturer evidence |
| --- | ---: | --- | --- | --- |
| `FER-360-SPIDER` | 2000 | Ferrari 360 Spider | Yes | [Reference](https://www.ferrari.com/en-BI/history/garage/2000/360-spider) |
| `FER-355-F1-GTS` | 1997 | Ferrari 355 F1 GTS | Yes | [Reference](https://www.ferrari.com/en-EN/history/garage/1997/355-f1-gts/1000) |
| `FER-348-TS` | 1989 | Ferrari 348 TS | Yes | [Reference](https://www.ferrari.com/en-ZM/history/garage/1989/348-ts) |
| `FER-348-SPIDER` | 1993 | Ferrari 348 Spider | Yes | [Reference](https://www.ferrari.com/en-IL/history/garage/1993/348-spider) |
| `FER-328-GTS` | 1985 | Ferrari 328 GTS | Yes | [Reference](https://www.ferrari.com/en-GQ/history/garage/1985/328-gts) |
| `FER-308-GTS-QV` | 1982 | Ferrari 308 GTS Quattrovalvole | Yes | [Reference](https://www.ferrari.com/en-OM/history/garage/1982/308-gts-quattrovalvole) |
| `FER-308-GTB-QV` | 1982 | Ferrari 308 GTB Quattrovalvole | Yes | [Reference](https://www.ferrari.com/en-HU/history/garage/1982/308-gtb-quattrovalvole) |
| `FER-DINO-246GTS` | 1972 | Ferrari Dino 246 GTS | Yes | [Reference](https://www.ferrari.com/en-MG/history/garage/1972/dino-246-gts) |
| `FER-LAF-APERTA` | 2016 | Ferrari LaFerrari Aperta | Yes | [Reference](https://cdn.ferrari.com/cms/network/media/pdf/2016_12_31_-_ferrari_nv_20f_0.pdf) |
| `FER-812-COMP-A` | 2021 | Ferrari 812 Competizione A | Yes | [Reference](https://cdn.ferrari.com/cms/network/media/pdf/cs_812_competizione_812_competizione_a_gbr_def.pdf) |
| `FER-SF90-XX-STRADALE` | 2023 | Ferrari SF90 XX Stradale | Yes | [Reference](https://www.ferrari.com/content/dam/ferrari-fcom/old/pdf/CS_SF90XXStradale_SF90XXSpider_ita_update.pdf) |
| `FER-SF90-XX-SPIDER` | 2023 | Ferrari SF90 XX Spider | Yes | [Reference](https://www.ferrari.com/content/dam/ferrari-fcom/old/pdf/CS_SF90XXStradale_SF90XXSpider_ita_update.pdf) |
| `FER-F80-ROAD` | 2024 | Ferrari F80 | Yes | [Reference](https://cdn.ferrari.com/cms/network/media/pdf/CS_Ferrari_Red_Dot_Awards_2025_eng.pdf) |
| `FER-FXX-TRACK` | 2005 | Ferrari FXX | No | [Reference](https://cdn.ferrari.com/cms/network/media/pdf/XXPROGRAMME_F1CLIENTI_Brochure_Ferrari.pdf) |
| `FER-FXX-K-TRACK` | 2014 | Ferrari FXX K | No | [Reference](https://cdn.ferrari.com/cms/network/media/pdf/XXPROGRAMME_F1CLIENTI_Brochure_Ferrari.pdf) |
| `FER-FXX-K-EVO` | 2017 | Ferrari FXX K Evo | No | [Reference](https://www.ferrari.com/en-UG/history/garage/2017/fxx-k-evo) |
| `FER-599XX-TRACK` | 2010 | Ferrari 599XX | No | [Reference](https://www.ferrari.com/zh-CN/magazine/articles/ferrari-collection-by-one-passionate-enthusiast) |
| `FER-599XX-EVO` | 2012 | Ferrari 599XX Evo | No | [Reference](https://cdn.ferrari.com/cms/network/media/pdf/XXPROGRAMME_F1CLIENTI_Brochure_Ferrari.pdf) |
| `LAM-AVE-LP700-ROAD` | 2012 | Lamborghini LP 700-4 Roadster | Yes | [Reference](https://preowned.lamborghini.com/en_us/models/aventador-roadster) |
| `LAM-AVE-SV-ROAD` | 2015 | Lamborghini LP 750-4 Superveloce Roadster | Yes | [Reference](https://preowned.lamborghini.com/en_gb/models/aventador-superveloce-roadster) |
| `LAM-REVENTON-ROAD` | 2009 | Lamborghini Reventón Roadster | Yes | [Reference](https://www.lamborghini.com/en-en/node/1064) |
| `LAM-CENT-ROAD` | 2016 | Lamborghini Centenario Roadster | Yes | [Reference](https://www.lamborghini.com/en-en/history/few-off/centenario-roadster) |
| `LAM-SIAN-ROAD` | 2020 | Lamborghini Sián Roadster | Yes | [Reference](https://www.lamborghini.com/en-en/models/few-off/sian-roadster) |
| `LAM-TEMERARIO-ROAD` | 2024 | Lamborghini Temerario | Yes | [Reference](https://www.lamborghini.com/en-en/models/temerario) |
| `LAM-GAL-LP560-SPY` | 2008 | Lamborghini LP 560-4 Spyder | Yes | [Reference](https://pictures.dealer.com/lamborghinilasvegas/8a3d4d8040463872006cffbb9450da2b.pdf) |
| `LAM-GAL-PERF-SPY` | 2010 | Lamborghini LP 570-4 Spyder Performante | Yes | [Reference](https://www.lamborghini.com/en-en/history/gallardo-lp-570-4-spyder-performante) |
| `LAM-GAL-ST-2009` | 2009 | Lamborghini Super Trofeo — original 2009 race car | No | [Reference](https://www.lamborghini.com/en-en/motorsport/motorsport-models/heritage) |
| `LAM-HUR-ST-620` | 2015 | Lamborghini LP 620-2 Super Trofeo — original race car | No | [Reference](https://www.lamborghini.com/en-en/motorsport/motorsport-models/heritage) |
| `LAM-HUR-STERRATO` | 2022 | Lamborghini Sterrato | Yes | [Reference](https://www.lamborghini.com/en-en/history/huracan-sterrato) |
| `LAM-COUNTACH-LPI` | 2021 | Lamborghini LPI 800-4 | Yes | [Reference](https://www.lamborghini.com/en-en/node/975) |
| `MCL-540C-COUPE` | 2015 | McLaren 540C Coupé | Yes | [Reference](https://mclaren-web.s3.eu-west-2.amazonaws.com/files/Owner%20Manual%20-%20Sports%20Series%20-%20Middle%20East%20and%20Africa%20-%20English.pdf) |
| `MCL-570GT-COUPE` | 2016 | McLaren 570GT | Yes | [Reference](https://cars.mclaren.com/us_en/legacy/570gt) |
| `MCL-GT-COUPE` | 2019 | McLaren GT | Yes | [Reference](https://www.mclarenofgreenwich.com/GT/) |
| `MCL-GTS-COUPE` | 2024 | McLaren GTS | Yes | [Reference](https://cars.mclaren.com/gl_en/gts) |
| `MCL-W1-ROAD` | 2024 | McLaren W1 | Yes | [Reference](https://cars.mclaren.com/gb-en/w1) |
| `MCL-P1-GTR-TRACK` | 2015 | McLaren P1 GTR | No | [Reference](https://cars.mclaren.com/gl_en/ultimate-models/mclaren-p1-gtr) |
| `MCL-SENNA-GTR` | 2019 | McLaren Senna GTR | No | [Reference](https://website-uat.mclaren.com/gl_en/ultimate-models/mclaren-senna-gtr/a-momentous-experience) |
| `MCL-SOLUS-GT` | 2022 | McLaren Solus GT | No | [Reference](https://cars.mclaren.com/us_en/mclaren-solus-gt) |
| `PAG-IMOLA-ROADSTER` | 2023 | Pagani Imola Roadster | Yes | [Reference](https://www.pagani.com/press/pagani-imola-roadster/) |
| `KOE-GEMERA-HV8` | 2023 | Koenigsegg Gemera HV8 | Yes | [Reference](https://www.koenigsegg.com/index.php/technical-specifications-gemera-2023) |
| `KOE-CCGT-TRACK` | 2007 | Koenigsegg CCGT — original GT1 prototype | No | [Reference](https://www.koenigsegg.com/model/ccgt) |
| `KOE-CCXR-TREVITA` | 2009 | Koenigsegg Trevita | Yes | [Reference](https://www.koenigsegg.com/model/ccxr-trevita) |
| `PAG-IMOLA-COUPE` | 2020 | Pagani Imola Coupé | Yes | [Reference](https://www.pagani.com/press/pagani-imola/) |
| `PAG-ZON-HP-BARCHETTA` | 2017 | Pagani HP Barchetta | Yes | [Reference](https://www.pagani.com/zonda-hp-barchetta/) |
| `PAG-HUA-R-EVO` | 2024 | Pagani R Evo Roadster | No | [Reference](https://www.pagani.com/press/huayra-r-evo-roadster/) |
| `HEN-F5-ROADSTER` | 2022 | Hennessey Roadster — original 1817 bhp | Yes | [Reference](https://www.hennesseyspecialvehicles.com/venom-f5-roadster/) |
| `FER-ROMA-SPIDER` | 2023 | Ferrari Roma Spider | Yes | [Reference](https://cdn.ferrari.com/cms/network/media/pdf/CS_Ferrari_Roma_Spider_final_GBR_rev.pdf) |
| `RIM-CONCEPTONE-2017` | 2017 | Rimac Concept_One — 2017 specification | Yes | [Reference](https://www.rimac-newsroom.com/press-releases/rimac-automobili/rimac-automobili-at-the-2017-geneva-motor-show) |
| `RIM-NEVERA-R` | 2024 | Rimac Nevera R — launch specification | Yes | [Reference](https://www.rimac-newsroom.com/press-releases/rimac-nevera-r/rimac-introduces-nevera-r-a-new-2107-hp-hypercar) |
| `SAL-S7-NA` | 2000 | Saleen S7 — naturally aspirated | Yes | [Reference](https://saleen.com/models/s7) |

## Photo attribution

All downloaded photos are unchanged copies of Commons-provided resized images.
The Trevita image is an existing cropped derivative; the original Commons page
retains its attribution history.

| Variant ID | Creator | License | Original file |
| --- | --- | --- | --- |
| `FER-360-SPIDER` | Handelsgeselschaft | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Ferrari_360_Spider_Toulouse.jpg) |
| `FER-355-F1-GTS` | Jiří Sedláček | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Ferrari_355_F1_GTS_1998_at_Legendy_2019_in_Prague.jpg) |
| `FER-348-TS` | Desty | Public domain | [Commons](https://commons.wikimedia.org/wiki/File:Ferrari_348_ts,_pre-facelift_model.jpg) |
| `FER-348-SPIDER` | MercurySable99 | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:1994_Ferrari_348_Spider,_front_left,_06-21-2026.jpg) |
| `FER-328-GTS` | Alexander Migl | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:1987_Ferrari_328_GTS_Paul_Pietsch_Classic_2025_DSC_9010.jpg) |
| `FER-308-GTS-QV` | Niels de Wit from Lunteren, The Netherlands | CC BY 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:1983_Ferrari_308_GTS_Quattrovalvole_(8971014515).jpg) |
| `FER-308-GTB-QV` | Cjp24 | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Ferrari_308_GTB_Quattrovalvole,_1984.jpg) |
| `FER-DINO-246GTS` | MrWalkr | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:1973_Ferrari_Dino_246_GTS_SP23.jpg) |
| `FER-LAF-APERTA` | Calreyn88 | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Ferrari_LaFerrari_Aperta_(31698).jpg) |
| `FER-812-COMP-A` | Calreyn88 | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:2023_Ferrari_812_Competizione_Aperta_4.jpg) |
| `FER-SF90-XX-STRADALE` | Mr.choppers | CC BY-SA 3.0 | [Commons](https://commons.wikimedia.org/wiki/File:2024_Ferrari_SF90_XX_Stradale_in_Bianco_Artico,_front_left.jpg) |
| `FER-SF90-XX-SPIDER` | Calreyn88 | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:2024_Ferrari_SF90_XX_Spider.jpg) |
| `FER-F80-ROAD` | Calreyn88 | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:2025_Ferrari_F80.jpg) |
| `FER-FXX-TRACK` | Ank kumar | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Ferrari_Enzo_FXX_(Ank_Kumar,_Infosys_Limited)_01.jpg) |
| `FER-FXX-K-TRACK` | emperornie | CC BY-SA 2.0 it | [Commons](https://commons.wikimedia.org/wiki/File:2015_Ferrari_FXX-K_in_Shanghai.jpg) |
| `FER-FXX-K-EVO` | Calreyn88 | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Ferrari_FXX-K_EVO_1.jpg) |
| `FER-599XX-TRACK` | Thesupermat | CC BY-SA 3.0 | [Commons](https://commons.wikimedia.org/wiki/File:Paris_-_RM_Auctions_-_5_f%C3%A9vrier_2014_-_Ferrari_599XX_-_2010_-_007.jpg) |
| `FER-599XX-EVO` | Alexandre Prévot from Nancy, France | CC BY-SA 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Ferrari_599XX_Evo_(21125892872).jpg) |
| `LAM-AVE-LP700-ROAD` | OWS Photography | CC BY 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Lamborghini_Aventador_Roadster_(LP700-4)_Greater_Toronto_Area,_Canada.jpg) |
| `LAM-AVE-SV-ROAD` | MrWalkr | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:2017_Lamborghini_Aventador_SV_Roadster_white.jpg) |
| `LAM-REVENTON-ROAD` | MrWalkr | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:2010_Lamborghini_Reventon_Roadster_Low.jpg) |
| `LAM-CENT-ROAD` | Alexander Migl | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Lamborghini_Centenario_Roadster_Retro_Classics_2020_IMG_0077.jpg) |
| `LAM-SIAN-ROAD` | MrWalkr | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:2021_Lamborghini_Sian_Roadster_TM26.jpg) |
| `LAM-TEMERARIO-ROAD` | Calreyn88 | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Lamborghini_Temerario_2025.jpg) |
| `LAM-GAL-LP560-SPY` | Axion23 | CC BY 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Lamborghini_Gallardo_LP560-4_Spyder_(8562694841).jpg) |
| `LAM-GAL-PERF-SPY` | Ben | CC BY-SA 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Lamborghini_Gallardo_LP570-4_Spyder_Performante_(6370389053).jpg) |
| `LAM-GAL-ST-2009` | AngMoKio | CC BY-SA 3.0 | [Commons](https://commons.wikimedia.org/wiki/File:Lamborghini_Super_Trofeo_22_2010_amk.JPG) |
| `LAM-HUR-ST-620` | Axion23 | CC BY 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Lamborghini_Huracan_Super_Trofeo_(15383668411).jpg) |
| `LAM-HUR-STERRATO` | MrWalkr | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:2023_Lamborghini_Huracan_Sterrato_Yellow.jpg) |
| `LAM-COUNTACH-LPI` | Calreyn88 | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Lamborghini_Countach_LPI_800-4.jpg) |
| `MCL-540C-COUPE` | Tokumeigakarinoaoshima | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:McLaren_540C_(M838TE)_front.jpg) |
| `MCL-570GT-COUPE` | Oleg Yunakov | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:2017_McLaren_570GT_-_02.jpg) |
| `MCL-GT-COUPE` | Matti Blume | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:McLaren_GT,_Klassikstadt,_Frankfurt_am_Main_(P1032520).jpg) |
| `MCL-GTS-COUPE` | Matti Blume | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:McLaren_GTS,_Frankfurt_am_Main_(P1032580).jpg) |
| `MCL-W1-ROAD` | MrWalkr | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:2024_McLaren_W1_SP25.jpg) |
| `MCL-P1-GTR-TRACK` | Ank Kumar | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:McLaren_P1_GTR_at_Grand_Basel_2018_04.jpg) |
| `MCL-SENNA-GTR` | Calreyn88 | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:McLaren_Senna_GTR.jpg) |
| `MCL-SOLUS-GT` | MrWalkr | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:2023_McLaren_Solus_GT.jpg) |
| `PAG-IMOLA-ROADSTER` | MrWalkr | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:2024_Pagani_Huayra_Imola_Roadster.jpg) |
| `KOE-GEMERA-HV8` | Alexander-93 | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Koenigsegg_Gemera_Auto_Zuerich_2023_1X7A1120.jpg) |
| `KOE-CCGT-TRACK` | Richard Bjerkøe ( w:User:SYnzYgUs ) | CC BY-SA 3.0 | [Commons](https://commons.wikimedia.org/wiki/File:Koenigsegg_CCGT.JPG) |
| `KOE-CCXR-TREVITA` | Axion23 (cropped derivative on Commons) | CC BY 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Koenigsegg_CCXR_Trevita_(20031267116)_cropped.jpg) |
| `PAG-IMOLA-COUPE` | Saggittarius A | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Pagani_Huayra_Imola_Milano_1.jpg) |
| `PAG-ZON-HP-BARCHETTA` | Y.Leclercq© | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Pagani_Zonda_HP_Barchetta.jpg) |
| `PAG-HUA-R-EVO` | Yu Chu Chin | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Pagani_Huayra_R_Evo_at_the_2026_Adelaide_Motorsport_Festival_(DSCF2554).jpg) |
| `HEN-F5-ROADSTER` | MrWalkr | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:2022_Hennessey_Venom_F5_Roadster.jpg) |
| `FER-ROMA-SPIDER` | Alexander-93 | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Ferrari_Roma_Spider_Auto_Zuerich_2023_1X7A1455.jpg) |
| `RIM-CONCEPTONE-2017` | Norbert Aepli, Switzerland ( User:Noebu ) | CC BY 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:2017-03-07_Geneva_Motor_Show_0932.JPG) |
| `RIM-NEVERA-R` | Matti Blume | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Rimac_Nevera_R,_Auto_2024,_Zurich_(PANA0591).jpg) |
| `SAL-S7-NA` | Semnoz at French Wikipedia | CC BY-SA 3.0 | [Commons](https://commons.wikimedia.org/wiki/File:SAG2004_181_Saleen.jpg) |

## Repeatable validation

```powershell
python scripts/import_supercars50.py
python scripts/import_supercars50.py --apply
python -m unittest test_startup test_jdm_import test_supercars_import -v
python export_public.py --output dist
```

The default import is read-only. On a pre-batch database it previews exactly 50
new profiles. Applying the exact manifest again makes no changes. A conflicting
batch digest, ID or normalized identity is rejected. Writes use one transaction
and roll back if public payload validation fails.

Regression tests exercise existing-row preservation, startup idempotence, repeat
imports, whole-batch collision rejection, read-only preview and rollback after an
export-validation failure. Final checks also compare every pre-existing table row
against the 345-car Git baseline, verify SQLite integrity and foreign keys, and
confirm that all 50 new IDs and local images appear in the public export.
