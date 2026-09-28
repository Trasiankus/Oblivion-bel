# REVIEW.md — праверка ўжо запоўненых `custom` (Крок 0.3)

Поўны вывад `scripts/validate.py` (усе працоўныя файлы) — 57 паведамленняў,
большасць з якіх тэхнічныя ілжывыя спрацоўванні (гл. «Не патрабуе праўкі»
ніжэй). Сапраўдныя памылкі ў ўжо запоўненых чалавекам `custom` — ніжэй.
Гэтыя палі НЕ змяняліся (правіла TASK.md: ужо запоўнены `custom` не чапаць).

## Сапраўдныя памылкі (патрабуюць увагі чалавека)

1. **`ST_FullNames/LOC_FN_SE03ObeliskStaff01`** (`different_...json`)
   `custom: "Крыштальны посаx"` — апошняя літара лацінская `x` замест
   беларускай `х`. Прапанова: `"Крыштальны посах"`.

2. **Сістэмная памылка тэга `<lf>` → `<cf>`.** Тэг `<cf>` НІКОЛІ не сустракаецца
   ў `en` (правераў ва ўсіх файлах) — гэта пашкоджаны варыянт `<lf>`
   (пераводу радка), які трапіў у чарнавыя `bel`/`bel_alt` (89 разоў у
   `ST_AltarDynamicTexts.json`, дзясяткі ў іншых файлах) і ўжо пранік
   у 4 гатовыя `custom`:
   - `ST_FullNames/LOC_FN_sFavoredAttributes_LEVEL0_F` — `<cf>` замест `<lf>`.
   - `ST_FullNames/LOC_FN_sMajorSkills_LEVEL0_F` — тое ж.
   - `ST_FullNames/LOC_FN_sReturnToMainMenu_LEVEL0_F` — тое ж.
   - `ST_AltarStaticTexts/LOC_AS_Magic_GlobalDetails_SpellEffectiveness` — тое ж.
   Прапанова: замяніць `<cf>` на `<lf>` ва ўсіх чатырох. Пры далейшай працы
   (Крок 2-4) тэгі заўсёды бяром з `en`, каб не пераносіць гэтую памылку з
   чарнавікоў — гэта ўжо ўлічана ў PROGRESS.md/workflow.

3. **`ST_FullNames/LOC_FN_sSpecialization_LEVEL0_F`** (`different_...json`)
   Пашкоджаны тэг: `< RT_BlueMed>` (лішні прабел пасля `<`) сустракаецца
   двойчы; таксама прапушчаны прабел перад адным `<RT_BlueMed>` пасля слова
   «бонус». Прапанова: выправіць на `<RT_BlueMed>` без прабелу і дадаць
   прабелы паміж словамі і тэгамі, як у `en`.

4. ~~**`ST_HardcodedContent/LOC_HC_MenuGamesettings_sMiscApprenticeSkills`**~~
   **ВЫПРАЎЛЕНА ў Кроку 4b, партыя 1**: запіс быў пусты на момант
   запаўнення (не «ужо запоўнены чалавекам», як меркавалася тут), выпраўлена
   на `"Навыкі вучня"`.

5. ~~**`ST_HardcodedContent/LOC_HC_EffectItemList_sMagicCostliestEffectSkillOf`**~~
   **ВЫПРАЎЛЕНА ў Кроку 4b, партыя 1**: запіс быў пусты на момант
   запаўнення, дададзены вядучы прабел як у `en` (`" Навык"`).

## Дробныя стылёвыя разыходжанні (нізкі прыярытэт, на меркаванне чалавека)

Наступныя ўжо запоўненыя `custom` заканчваюцца не тым знакам прыпынку,
што `en` (часцей за ўсё чалавек проста не паставіў кропку ў канцы, або
наадварот дадаў кропку/пытальнік, якога няма ў `en`). Гэта не блакуе
працу і пакінута без змен:
`ST_FullNames/LOC_FN_MS45WaitTopic`, `ST_FullNames/LOC_FN_responseRoadWarning`,
`ST_FullNames/LOC_FN_sDiscoveredText_LEVEL0_F`, `ST_FullNames/LOC_FN_sLevelUp17_LEVEL0_F`,
`ST_FullNames/LOC_FN_sMiscNumPlacesDiscovered_LEVEL0_F`, `ST_FullNames/LOC_FN_sMiscSEBounty_LEVEL0_F`,
`ST_FullNames/LOC_FN_sOpenWithKey_LEVEL0_F`,
`ST_AltarStaticTexts/LOC_AS_CharacterCreation_SliderInfo_Low`,
`ST_AltarStaticTexts/LOC_AS_CharacterCreation_SliderInfo_Salt&Pepper`,
`ST_AltarStaticTexts/LOC_AS_Generic_Notification_NoSpecialCharacters`,
`ST_AltarStaticTexts/LOC_AS_Magic_BodyText_CanOnlyBeCastOnce`,
`ST_AltarStaticTexts/LOC_AS_Magic_BodyText_ImmuneToSilence`,
`ST_AltarStaticTexts/LOC_AS_Quests_QuestLog_Quest_MSShadowscale_STAGE200`,
`ST_HardcodedContent/LOC_HC_EffectItem_sMagicEffectItemSecondsPlural`,
`ST_HardcodedContent/LOC_HC_EffectItem_sMagicEffectItemSecondsSingular`,
`ST_HardcodedContent/LOC_HC_MagicItem_sMagicCastInsufficientMagicka`,
`ST_HardcodedContent/LOC_HC_MagicItem_sMagicCastInsufficientSkill`,
`ST_HardcodedContent/LOC_HC_MagicItem_sMagicCastPowerUsed`,
`ST_HardcodedContent/LOC_HC_MagicItem_sMagicCastRangedUnderwater`,
`ST_HardcodedContent/LOC_HC_MenuGamesettings_sAddItemtoInventory`,
`ST_HardcodedContent/LOC_HC_MenuGamesettings_sAddItemtoSpellList`,
`ST_MissingEntries/LOC_ME_ContractedDisease` (дадана кропка — нармальна),
`ST_MissingEntries/LOC_ME_EquipItemOnPlayerMessage`,
`ST_MissingEntries/LOC_ME_GenericMenu_SkillIncrease`,
`ST_MissingEntries/LOC_ME_ItemAddedToSpellList`,
`ST_MissingEntries/LOC_ME_ItemRemovedFromInventory`,
`ST_MissingEntries/LOC_ME_LevelUp_ChooseAttributesToIncrease`,
`ST_MissingEntries/LOC_ME_PoisonBowConfirmMessage` (дададзены «?» — нармальна),
`ST_MissingEntries/LOC_ME_PoisonWeaponConfirmMessage` (тое ж),
`ST_MissingEntries/LOC_ME_PotionCreatedMessage`,
`ST_MissingEntries/LOC_ME_TriedPickPocket`,
`ST_MissingEntries/LOC_ME_UnEquipItemOnPlayerMessage`.

`ST_HardcodedContent/LOC_HC_EffectItemList_sMagicCostliestEffectSkillOf` —
прабел у пачатку/канцы не супадае з `en` (гл. п.5 вышэй).

## Крок 2 (`same_bel_belalt_case_insensitive.json`) — заўвагі

Усе 6493 пустыя запісы запоўнены скрыптам (гл. PROGRESS.md). `validate.py`
дадаткова паказвае 21 «памылку» лацінкі — гэта тэхнічныя ID распрацоўшчыкаў
і лацінскія ўласныя назвы (маркі віна, коды NPC/DLC), скапіраваныя
verbatim з `bel`/`bel_alt` (там `bel == bel_alt`, механічны выпадак не
чапаўся): `BattlehornWineBarrelA/C/E` (маркі віна "Frostdew Blanc" і інш.),
`Book2CommonShortLifeUrielSeptim` (рымская лічба "VII"), `Dark05Convo`,
`Dark09Speech`, `FGC06GoblinFaction`, `NDConvSysImperialFNPC`,
`NDEmilNPC1`, `NDUmarilVoiceNPC`, `NQDSkingrad`, `SE09Ceremony`,
`SEBookSixteenAccordsofMadnessV6/V9/V12` (рымскія лічбы), `SEYngvarFaction`,
`TestErik`, `lyndacarter` — усе тэхнічныя, не гульнявы тэкст. Не патрабуе праўкі.

## Не патрабуе праўкі (ілжывыя спрацоўванні `validate.py`, пакінуты для даведкі)

- Лацінская літара `x` як лічбавы плэйсхолдэр (напр. `"x damage!"` →
  `"x шкоды!"`) — гэта не тэг у `<>`/`{}`, але ў гульні падстаўляецца
  сапраўднае значэнне; пакінута як у `en`.
- Тэхнічныя абрэвіятуры лацінкай усярэдзіне беларускага тэксту:
  `NPC`, `MQ10`, `getincell`, `DLC06Fletcher1` і да т.п. — распрацоўніцкія
  ідэнтыфікатары/каментарыі, не гульнявы тэкст для гульца.
  (`ST_FullNames/LOC_FN_AbBirthsignNPCMage`, `ST_FullNames/LOC_FN_MQ10BrumaOblivion`,
  `ST_FullNames/LOC_FN_MQ10BurdSpeech`, і серыя `LOC_FN_SE*ObeliskStaff0N`
  акрамя SE03ObeliskStaff01 — гл. п.1).
- Разыходжанне колькасці формаў у ICU `|plural(...)`/`|ordinal(...)` паміж
  `en` і `custom` — беларуская патрабуе больш формаў (`one/few/many/other`),
  чым англійская (`one/other`), гэта чакана і ўлічана ў `validate.py`.

## Статыстыка (на момант праверкі, да пачатку Кроку 1)

- `same_bel_belalt_case_insensitive.json`: 6531 запісаў, запоўнена 38, пуста 6493.
- `different_bel_belalt_case_insensitive.json`: 15274 запісаў, запоўнена 2106, пуста 13168.
- `ST_AltarDynamicTexts.json`: 1284 запісаў, запоўнена 5, пуста 1279.
- `ST_AltarStaticTexts.json`: 275 запісаў, запоўнена 275 (усе).
- `ST_HardcodedContent.json`: 829 запісаў, запоўнена 168, пуста 661.
- `ST_MissingEntries.json`: 71 запіс, запоўнена 71 (усе).
