# F-003 — LAW 7.14 case data model: entities and system field catalog

**Research questions:** RQ-ING-01 (case/custodian/source identifiers), RQ-ING-02 (hashes, processing history), RQ-ING-05 (dedup relationships), RQ-EXC-01 (exception records), RQ-NUM-01.
**Target:** LAW 7.14.290 (ART-110). **Method:** REA `inspect-managed-artifact` listed 343 embedded SQL resources in the schema-manager assembly; the case-creation and ED-enable scripts were read to enumerate entities and field definitions. Script text is **not** reproduced here; only externally meaningful entity names, field names, and documented type semantics are kept (these are the field names a LAW operator sees and exports).
**Evidence:** OBSERVED (schema), DOCUMENTED (field-type semantics from LAW 6.2.46 User Guide, EV-001). Nothing executed.

## Entities (OBSERVED, paraphrased)

| Entity | Role | Notable attributes |
|---|---|---|
| Volume | Physical image/text storage root | id, path |
| Document | One record per document | page count, volume, relative path, document order, image extension, OCR status, attachment parent id + attachment level, creator user, created timestamp, duplicate-custodian names/paths, duplicate-parent name/path, bookmark/annotation/redaction flags, OCR accuracy, text file path, GUID |
| Page | One record per page image | document id, page number, page filename, up to three unique ids, header/footer flags, OCR flag, orphan flag, source/color/page-size ids, width, height, redaction flag |
| Field definition | Self-describing field registry | name, type code, display order, span height, length, custom/locked/page-level/system/indexed/unique/visible flags, references, display-as, extended-property flag, category |
| Case properties | key/value settings | name, value |
| ED (electronic discovery) extension | Added when a case is "ED-enabled" | Custodians, ED Sessions, ED Sources, Folders, Duplicate log, Extended properties, Time zones, Body (full text) |

Management database (separate): case registry and project registry.

## Documented field type codes (DOCUMENTED, LAW 6.2.46 UG)

`0` Text (≤255 chars, page or document) · `1` Auto-Increment · `2` List · `3` Memo (document only; not indexable) · `4` Date (mm/dd/yyyy) · `5` Numeric (int32) · `6` Tag (Y/N) · `7` Tiny Int. Codes `8`, `10`, `11` appear in 7.14 field definitions but are not in the 6.2 chart. Cross-referencing the LAW 7.x Answer Center *Field Descriptions* table (EV-015): fields with code `11` are described as **BigInt** (Filesize) — DOCUMENTED; fields with code `8` (ThreadID, IsRedacted, Language) are described as **Text** — DOCUMENTED type family, so `8` is INFERRED to be a second text storage variant (Unicode/long text); code `10` occurs only on reference ids (CustodianID, EDSessionID, EDSourceID, EDFolderID, TimeZoneID, ImportSetId) that the *Field Descriptions* page does not list — **UNKNOWN**, INFERRED to be an integer reference type. Code `7` (Tiny Int) covers the per-stage `_PS_*` flags, FileAccuracy, DateSource, _DupMethod, _FTIndex.

## System / ED field catalog (OBSERVED names; type per code above)

Identity & lineage: DocID (text 50), EdaID, CustodianID, EDSessionID, EDSourceID, EDFolderID, ImportSetId, ImportStation, BatchStation, _GUID (text 36), _DocCat, DeletePending.
File identity: Filename (memo), Filesize (code 11), DocExt / OrigExt (text 255), SuspectExt, SuspectOLE (tag-like text 1), FileType (numeric), FileDescription (text 50), FileAccuracy (tiny int), SourceApp (list 25), NativeFile, SourceFile (memo), Password (text 100), Placeholder_Name (list 255), HasPageLimit.
Hashes & dedup: MD5Hash (text 32), Sha1Hash (text 40), _DupID, DupStatus (text 1), _DupMethod, DupCustNames, DupCustPaths, DupParentName, DupParentPath (memo).
Processing status: TiffStatus, TextXStatus (extracted text), TextPStatus (printed text), OcrAccuracy, ErrorMsg, PrevErrMsg (memo), EDPages, HasExtProps, HiddenText (tag), _PS_OLEX/_PS_ARCX/_PS_EMBEDX/_PS_ATTX/_PS_DIGESTX/_PS_NATIVEX/_PS_MDX (per-stage tiny-int status flags: OLE, archive, embedded, attachment, digest, native, metadata — purpose INFERRED from names), PrintJobName.
Document metadata: Title, Subject, Author, LastAuthor (text 255), Keywords, Comments, Categories, Organization (memo), ApplicationName (text 50), Template (text 255), Revision (text 20), DateCreated/TimeCreated, DateLastMod/TimeLastMod, DateAccessed/TimeAccessed, DateLastPrnt/TimeLastPrnt (date + text-20 time pairs), DateLowerBound/DateUpperBound (+Time), DateSource, TimeZoneID, Language.
E-mail: EMailClient (text 15), EMail_Subject (memo), From (text 450), To, CC, BCC, Attach (memo), Importance (text 6), Sensitivity (text 12), DateSent/TimeSent, DateRcvd/TimeRcvd, Conversation, ConversationIndex (memo), ThreadID, EntryID, IntMsgID, InReplyToID (memo), Unread, ReadReceipt, DelivReceipt, MsgClass (text 128), Headers (memo), DateAppStart/End (+Time), FromDomain.
Short-message / mobile (7.x additions): CommunicationType, CommunicationStatus, Imei, DailyThreadId, MasterThreadId, ContactFrom, ContactTo, CallDuration, SourcePhoneNumbers, MsgDeleted.
Page/document display: IsRedacted (page-level), HasRedaction, HasAnnotations, HasBookmarks, BookmarkName, TextFilePath, _FTIndex.

## Observations relevant to requirements

1. **Dates and times are stored as separate Date and Text(20) Time fields** (DateCreated + TimeCreated, DateSent + TimeSent …) with a per-document TimeZoneID and a time-zone table → REQ-ING-004 must preserve original timestamp + zone and be able to emit split date/time columns for LAW/Concordance-style DAT consumers.
2. **Two hashes (MD5, SHA-1) per document plus a dedup method and dedup id**, with duplicate custodian/parent names *and paths* retained on the surviving record → REQ-ING-005 (dedup retains source/custodian relationships) is corroborated by the reference product's model.
3. **Per-stage status flags and an error/previous-error pair per document** → exceptions are first-class per-document records, not just logs (REQ-EXC-001).
4. **Attachment relationships use parent id + attachment level**, i.e., a tree with depth → family handling (REQ-EXP-00x) needs depth, not just parent.
5. **Extracted-text status and printed-text status are distinct** → text provenance (native-extracted vs rendered/printed vs OCR) is tracked separately (REQ-TXT-001).
6. Page records carry per-page OCR flag, orientation-independent width/height, color id, redaction flag → page-level QC data model.

## Limitations

- Static schema reading; semantics of flag values (e.g., DupStatus letters, status codes) are UNKNOWN until documentation or runtime observation confirms them.
- Explore (EDA) schema (Inventory items, Jobs, Exports, Export errors, Import sessions…) was enumerated but not analysed; it is a sibling product database and out of first-release scope.
