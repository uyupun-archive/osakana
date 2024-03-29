import { type FunctionalComponent, type JSX } from 'preact';
import { useEffect, useState } from 'preact/hooks';

import {
  addReadingListRecord,
  searchReadingList,
  fishingReadingListRecord,
  readReadingListRecord,
  unreadReadingListRecord,
  deleteReadingListRecord,
  bookmarkReadingListRecord,
  getReadingListCounts,
  exportReadingList,
  importReadingList,
} from '../../api/endpoints/readingList';
import {
  UrlNotFoundError,
  UrlAlreadyExistsError,
  ReadingListRecordTypeError,
  ReadingListRecordNotFoundError,
  ReadingListRecordAlreadyReadError,
  ReadingListRecordNotYetReadError,
  ReadingListCountsTypeError,
  ExportReadingListRecordTypeError,
  EmptyFileError,
  FileSizeLimitExceededError,
  InvalidFileExtensionError,
  InvalidJsonContentsError,
  InvalidJsonStructureError,
  ExportReadingListRecordParseError,
  ReadingListRecordDuplicateError,
} from '../../api/errors';
import LogoWithText from '../../assets/logo-with-text.svg';
import NoImage from '../../assets/no-image.svg';
import { InvalidHttpUrlError } from '../../errors';

import type {
  Uuid4,
  ReadingList,
  ReadingListRecord as ReadingListRecordProps,
  ReadingListSearchFilters,
  ReadingListCounts,
} from '../../types';
import './home.css';

export const Home = (): JSX.Element => {
  enum ReadFilter {
    ALL = 'all',
    READ = 'read',
    UNREAD = 'unread',
  }

  const parseReadFilter = (value: string): ReadFilter => {
    switch (value) {
      case ReadFilter.ALL:
        return ReadFilter.ALL;
      case ReadFilter.READ:
        return ReadFilter.READ;
      case ReadFilter.UNREAD:
        return ReadFilter.UNREAD;
      default:
        throw new InvalidReadFilterError();
    }
  };

  class InvalidReadFilterError extends Error {
    constructor() {
      const message = 'Invalid read filter error';
      super(message);
      this.name = 'InvalidReadFilterError';
      Object.setPrototypeOf(this, new.target.prototype);
    }
  }

  const [importedReadingList, setImportedReadingList] = useState<File | null>(null);
  const [isImportLoading, setIsImportLoading] = useState<boolean>(false);
  const [importedReadingListMessage, setImportedReadingListMessage] = useState<string | null>(null);
  const [inputAddForm, setInputAddForm] = useState<string>('');
  const [isAddLoading, setIsAddLoading] = useState<boolean>(false);
  const [inputAddFormMessage, setInputAddFormMessage] = useState<string | null>(null);
  const [inputSearchForm, setInputSearchForm] = useState<string>('');
  const [bookmarkedFilter, setBookmarkedFilter] = useState<boolean>(false);
  const [readFilter, setReadFilter] = useState<ReadFilter>(ReadFilter.ALL);
  const [inputSearchErrorMessage, setInputSearchErrorMessage] = useState<string | null>(null);
  const [readingList, setReadingList] = useState<ReadingList>([]);
  const [readingListCounts, setReadingListCounts] = useState<ReadingListCounts>({
    total: 0,
    reads: 0,
    unreads: 0,
    bookmarks: 0,
  });

  const handleExportReadingList = async (): Promise<void> => {
    let res;
    try {
      res = await exportReadingList();
    } catch (e: unknown) {
      if (e instanceof ExportReadingListRecordTypeError) {
        console.error(e.message);
        return;
      }
      console.error('Unknown error');
    }

    const readingListJson = JSON.stringify(res);
    const readingListBlob = new Blob([readingListJson], { type: 'application/json' });
    const exportUrl = URL.createObjectURL(readingListBlob);

    const exportLink = document.createElement('a');
    exportLink.href = exportUrl;
    exportLink.download = 'reading-list.json';
    exportLink.style.display = 'none';
    document.body.appendChild(exportLink);
    exportLink.click();
    document.body.removeChild(exportLink);
  };

  const handleSelectImportReadingList = (e: Event): void => {
    const target = e.target as HTMLInputElement;
    if (target.files != null) {
      setImportedReadingList(target.files[0]);
    }
  };

  const handleUploadImportReadingList = async (): Promise<void> => {
    setIsImportLoading(true);
    if (importedReadingList == null) {
      setImportedReadingListMessage('No file selected');
      return;
    }
    setImportedReadingListMessage('Uploading ...');
    const formData = new FormData();
    formData.append('file', importedReadingList, importedReadingList.name);
    try {
      await importReadingList(formData);
      setImportedReadingListMessage('Uploaded');
    } catch (e: unknown) {
      if (e instanceof EmptyFileError) {
        setImportedReadingListMessage(e.message);
        return;
      }
      if (e instanceof ReadingListRecordDuplicateError) {
        setImportedReadingListMessage(e.message);
        return;
      }
      if (e instanceof FileSizeLimitExceededError) {
        setImportedReadingListMessage(e.message);
        return;
      }
      if (e instanceof InvalidFileExtensionError) {
        setImportedReadingListMessage(e.message);
        return;
      }
      if (e instanceof InvalidJsonContentsError) {
        setImportedReadingListMessage(e.message);
        return;
      }
      if (e instanceof InvalidJsonStructureError) {
        setImportedReadingListMessage(e.message);
        return;
      }
      if (e instanceof ExportReadingListRecordParseError) {
        setImportedReadingListMessage(e.message);
        return;
      }
      setImportedReadingListMessage('Unknown error');
    } finally {
      setIsImportLoading(false);
    }
  };

  const handleInputAddForm = (e: Event): void => {
    const target = e.target as HTMLInputElement;
    setInputAddForm(target.value);
  };

  const handleAddReadingListRecord = async (): Promise<void> => {
    const url = inputAddForm;
    setIsAddLoading(true);
    setInputAddFormMessage('Adding ...');
    try {
      await addReadingListRecord(url);
      setInputAddFormMessage('Added');
    } catch (e: unknown) {
      if (e instanceof InvalidHttpUrlError) {
        setInputAddFormMessage(e.message);
        return;
      }
      if (e instanceof UrlNotFoundError) {
        setInputAddFormMessage(e.message);
        return;
      }
      if (e instanceof UrlAlreadyExistsError) {
        setInputAddFormMessage(e.message);
        return;
      }
      setInputAddFormMessage('Unknown error');
    } finally {
      setInputAddForm('');
      setIsAddLoading(false);
    }
  };

  const handleInputSearchForm = (e: Event): void => {
    const target = e.target as HTMLInputElement;
    setInputSearchForm(target.value);
  };

  const handleSearchReadingList = async (): Promise<void> => {
    const keyword = inputSearchForm;
    const filters: ReadingListSearchFilters = {};
    if (bookmarkedFilter) {
      filters.is_bookmarked = true;
    }
    if (readFilter === 'read') {
      filters.is_read = true;
    }
    if (readFilter === 'unread') {
      filters.is_unread = true;
    }
    try {
      const res = await searchReadingList(keyword, filters);
      setInputSearchErrorMessage(null);
      setReadingList(res);
    } catch (e: unknown) {
      if (e instanceof ReadingListRecordTypeError) {
        setInputSearchErrorMessage(e.message);
        return;
      }
      setInputSearchErrorMessage('Unknown error');
    }
  };

  const handleFishingReadingListRecord = async (): Promise<void> => {
    try {
      const res = await fishingReadingListRecord();
      setInputSearchErrorMessage(null);
      setReadingList([res]);
    } catch (e: unknown) {
      if (e instanceof ReadingListRecordTypeError) {
        setInputSearchErrorMessage(e.message);
        return;
      }
      setInputSearchErrorMessage('Unknown error');
    }
  };

  const handleBookmarkedFilter = (e: Event): void => {
    const target = e.target as HTMLInputElement;
    setBookmarkedFilter(target.checked);
  };

  const handleReadFilter = (e: Event): void => {
    const target = e.target as HTMLInputElement;
    setReadFilter(parseReadFilter(target.value));
  };

  const handleReadingListCounts = async (): Promise<void> => {
    try {
      const res = await getReadingListCounts();
      setReadingListCounts(res);
    } catch (e: unknown) {
      if (e instanceof ReadingListCountsTypeError) {
        console.error(e.message);
        return;
      }
      console.error('Unknown error');
    }
  };

  useEffect(() => {
    handleReadingListCounts().catch(() => {});
  }, [readingList]);

  return (
    <>
      <img src={LogoWithText} alt="Osakana logo with text" width="500" />
      <div>
        <input type="file" onChange={handleSelectImportReadingList} />
        <button
          type="button"
          onClick={() => {
            void handleUploadImportReadingList();
          }}
          disabled={isImportLoading}
        >
          Import
        </button>
        <button type="button" onClick={handleExportReadingList}>
          Export
        </button>
        {importedReadingListMessage != null ? <div>{importedReadingListMessage}</div> : null}
      </div>
      <div>
        <input
          type="text"
          placeholder="https://..."
          value={inputAddForm}
          onChange={handleInputAddForm}
        />
        <button type="button" onClick={handleAddReadingListRecord} disabled={isAddLoading}>
          Add
        </button>
        {inputAddFormMessage != null ? <div>{inputAddFormMessage}</div> : null}
      </div>
      <div>
        <input
          type="text"
          placeholder="Keyword"
          value={inputSearchForm}
          onChange={handleInputSearchForm}
        />
        <button type="button" onClick={handleSearchReadingList}>
          Search
        </button>
        <button type="button" onClick={handleFishingReadingListRecord}>
          Fishing
        </button>
        <div>
          <input type="checkbox" checked={bookmarkedFilter} onChange={handleBookmarkedFilter} />
          <label>Bookmarked</label>
        </div>
        <div>
          <input
            type="radio"
            value={ReadFilter.ALL}
            checked={readFilter === ReadFilter.ALL}
            onChange={handleReadFilter}
          />
          <label>All</label>
          <input
            type="radio"
            value={ReadFilter.READ}
            checked={readFilter === ReadFilter.READ}
            onChange={handleReadFilter}
          />
          <label>Read</label>
          <input
            type="radio"
            value={ReadFilter.UNREAD}
            checked={readFilter === ReadFilter.UNREAD}
            onChange={handleReadFilter}
          />
          <label>Unread</label>
        </div>
        {inputSearchErrorMessage != null ? <div>{inputSearchErrorMessage}</div> : null}
      </div>
      <div>
        Total: {readingListCounts.total} ( Reads: {readingListCounts.reads} / Unreads:{' '}
        {readingListCounts.unreads} / Bookmarks: {readingListCounts.bookmarks})
      </div>
      {readingList.length <= 0 && <p>No records</p>}
      {readingList.length > 0 && (
        <table style={{ border: '1px solid black' }}>
          <thead>
            <tr>
              <th>Icon</th>
              <th>Title</th>
              <th>Created at</th>
              <th>Is read</th>
              <th>Is bookmarked</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {readingList.map((readingListRecord: ReadingListRecordProps) => (
              <ReadingListRecord
                key={readingListRecord.id}
                id={readingListRecord.id}
                url={readingListRecord.url}
                title={readingListRecord.title}
                isRead={readingListRecord.isRead}
                isBookmarked={readingListRecord.isBookmarked}
                thumb={readingListRecord.thumb}
                createdAt={readingListRecord.createdAt}
                updatedAt={readingListRecord.updatedAt}
                readAt={readingListRecord.readAt}
                bookmarkedAt={readingListRecord.bookmarkedAt}
                onReadingListRecordUpdated={handleSearchReadingList}
              />
            ))}
          </tbody>
        </table>
      )}
    </>
  );
};

const ReadingListRecord: FunctionalComponent<
  ReadingListRecordProps & { onReadingListRecordUpdated: () => Promise<void> }
> = (props) => {
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleReadReadingListRecord = async (id: Uuid4): Promise<void> => {
    setIsLoading(true);
    try {
      await readReadingListRecord(id);
      await props.onReadingListRecordUpdated();
    } catch (e: unknown) {
      if (
        e instanceof ReadingListRecordAlreadyReadError ||
        e instanceof ReadingListRecordNotFoundError
      ) {
        console.error(e.message);
      }
      console.error('Unknown error');
    }
    setIsLoading(false);
  };

  const handleUnreadReadingListRecord = async (id: Uuid4): Promise<void> => {
    setIsLoading(true);
    try {
      await unreadReadingListRecord(id);
      await props.onReadingListRecordUpdated();
    } catch (e: unknown) {
      if (
        e instanceof ReadingListRecordNotYetReadError ||
        e instanceof ReadingListRecordNotFoundError
      ) {
        console.error(e.message);
      }
      console.error('Unknown error');
    }
    setIsLoading(false);
  };

  const handleDeleteReadingListRecord = async (id: Uuid4): Promise<void> => {
    setIsLoading(true);
    try {
      await deleteReadingListRecord(id);
      await props.onReadingListRecordUpdated();
    } catch (e: unknown) {
      if (e instanceof ReadingListRecordNotFoundError) {
        console.error(e.message);
      }
      console.error('Unknown error');
    }
    setIsLoading(false);
  };

  const handleBookmarkReadingListRecord = async (id: Uuid4): Promise<void> => {
    setIsLoading(true);
    try {
      await bookmarkReadingListRecord(id);
      await props.onReadingListRecordUpdated();
    } catch (e: unknown) {
      if (e instanceof ReadingListRecordNotFoundError) {
        console.error(e.message);
      }
      console.error('Unknown error');
    }
    setIsLoading(false);
  };

  return (
    <tr
      style={{
        backgroundColor: props.isBookmarked ? '#ffd6d6' : !props.isRead ? '#d6eaff' : '',
      }}
    >
      <td>
        {props.thumb != null ? (
          <img src={props.thumb} alt={`${props.title} icon`} width="30" />
        ) : (
          <img src={NoImage} alt="No image" width="30" />
        )}
      </td>
      <td>
        <a href={props.url} target="_blank" rel="noreferrer noopener">
          {props.title}
        </a>
      </td>
      <td>{props.createdAt.toLocaleString()}</td>
      <td>
        {props.isRead && <span>Read ({props.readAt?.toLocaleString()})</span>}
        {!props.isRead && <span>Unread</span>}
      </td>
      <td>
        {props.isBookmarked && <span>Bookmarked ({props.bookmarkedAt?.toLocaleString()})</span>}
        {!props.isBookmarked && <span>-</span>}
      </td>
      <td>
        {!props.isRead && (
          <button
            type="button"
            onClick={async () => {
              await handleReadReadingListRecord(props.id);
            }}
            disabled={isLoading}
          >
            Read
          </button>
        )}
        {props.isRead && (
          <button
            type="button"
            onClick={async () => {
              await handleUnreadReadingListRecord(props.id);
            }}
            disabled={isLoading}
          >
            Unread
          </button>
        )}
        <button
          type="button"
          onClick={async () => {
            await handleDeleteReadingListRecord(props.id);
          }}
          disabled={isLoading}
        >
          Delete
        </button>
        <button
          type="button"
          onClick={async () => {
            await handleBookmarkReadingListRecord(props.id);
          }}
          disabled={isLoading}
        >
          Toggle bookmark
        </button>
      </td>
    </tr>
  );
};
