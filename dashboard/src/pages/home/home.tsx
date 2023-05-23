import { FunctionalComponent, JSX } from 'preact';
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
} from '../../api/endpoints/readingList';
import type {
  Uuid4,
  ReadingList,
  ReadingListRecord as ReadingListRecordProps,
  ReadingListSearchFilters,
  ReadingListCounts,
} from '../../types';
import { InvalidHttpUrlError } from '../../errors';
import {
  UrlNotFoundError,
  UrlAlreadyExistsError,
  ReadingListRecordTypeError,
  ReadingListRecordNotFoundError,
  ReadingListRecordAlreadyReadError,
  ReadingListRecordNotYetReadError,
  ReadingListCountsTypeError,
} from '../../api/errors';
import LogoWithText from '../../assets/logo-with-text.svg';
import NoImage from '../../assets/no-image.svg';
import './home.css';

export const Home = (): JSX.Element => {
  enum ReadFilter {
    ALL = 'all',
    READ = 'read',
    UNREAD = 'unread',
  };

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
    };
  }

  const [inputAddForm, setInputAddForm] = useState<string>('');
  const [inputAddFormMessage, setInputAddFormMessage] = useState<string | null>(null);
  const [inputSearchForm, setInputSearchForm] = useState<string>('');
  const [bookmarkedFilter, setBookmarkedFilter] = useState<boolean>(false);
  const [readFilter, setReadFilter] = useState<ReadFilter>(ReadFilter.ALL);
  const [inputSearchErrorMessage, setInputSearchErrorMessage] = useState<string | null>(null);
  const [readingList, setReadingList] = useState<ReadingList>([]);
  const [readingListCounts, setReadingListCounts] = useState<ReadingListCounts>({total: 0, reads: 0, unreads: 0, bookmarks: 0});

  const handleInputAddForm = (e: Event): void => {
    const target = e.target as HTMLInputElement;
    setInputAddForm(target.value);
  };

  const handleAddReadingListRecord = async (): Promise<void> => {
    const url = inputAddForm;
    setInputAddFormMessage("Adding ...");
    try {
      await addReadingListRecord(url);
      setInputAddFormMessage("Added");
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
    if (readFilter == 'read') {
      filters.is_read = true;
    }
    if (readFilter == 'unread') {
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
        console.log(e.message);
        return;
      }
      console.log('Unknown error');
    }
  };

  useEffect(() => {
    handleReadingListCounts();
  }, [readingList]);

  return (
    <>
      <img src={LogoWithText} alt="Osakana logo with text" width="500" />
      <div>
				<input type="text" placeholder="https://..." value={inputAddForm} onChange={handleInputAddForm} />
				<button type="button" onClick={handleAddReadingListRecord}>Add</button>
        {inputAddFormMessage && <div>{inputAddFormMessage}</div>}
			</div>
      <div>
				<input type="text" placeholder="Keyword" value={inputSearchForm} onChange={handleInputSearchForm} />
				<button type="button" onClick={handleSearchReadingList}>Search</button>
				<button type="button" onClick={handleFishingReadingListRecord}>Fishing</button>
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
        {inputSearchErrorMessage && <div>{inputSearchErrorMessage}</div>}
			</div>
      <div>
        Total: {readingListCounts.total} (
          Reads: {readingListCounts.reads} /
          Unreads: {readingListCounts.unreads} /
          Bookmarks: {readingListCounts.bookmarks}
        )
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

const ReadingListRecord: FunctionalComponent<ReadingListRecordProps & {onReadingListRecordUpdated: () => Promise<void>}> = (props) => {
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleReadReadingListRecord = async (id: Uuid4): Promise<void> => {
    setIsLoading(true);
    try {
      await readReadingListRecord(id);
      await props.onReadingListRecordUpdated();
    } catch (e: unknown) {
      if ((e instanceof ReadingListRecordAlreadyReadError) || (e instanceof ReadingListRecordNotFoundError)) {
        console.log(e.message);
      }
      console.log('Unknown error');
    }
    setIsLoading(false);
  };

  const handleUnreadReadingListRecord = async (id: Uuid4): Promise<void> => {
    setIsLoading(true);
    try {
      await unreadReadingListRecord(id);
      await props.onReadingListRecordUpdated();
    } catch (e: unknown) {
      if ((e instanceof ReadingListRecordNotYetReadError) || (e instanceof ReadingListRecordNotFoundError)) {
        console.log(e.message);
      }
      console.log('Unknown error');
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
        console.log(e.message);
      }
      console.log('Unknown error');
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
        console.log(e.message);
      }
      console.log('Unknown error');
    }
    setIsLoading(false);
  };

  return (
    <tr style={{
      backgroundColor:
        props.isBookmarked
          ? '#ffd6d6'
        :!props.isRead
          ? '#d6eaff'
          : ''
    }}>
      <td>
        {!props.thumb && <img src={NoImage} alt="No image" width="30" />}
        {props.thumb && <img src={props.thumb} alt={`${props.title} icon`} width="30" />}
      </td>
      <td>
        <a href={props.url} target="_blank" rel="noreferrer noopener">{props.title}</a>
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
        {!props.isRead && <button type="button" onClick={() => handleReadReadingListRecord(props.id)} disabled={isLoading}>Read</button>}
        {props.isRead && <button type="button" onClick={() => handleUnreadReadingListRecord(props.id)} disabled={isLoading}>Unread</button>}
        <button type="button" onClick={() => handleDeleteReadingListRecord(props.id)} disabled={isLoading}>Delete</button>
        <button type="button" onClick={() => handleBookmarkReadingListRecord(props.id)} disabled={isLoading}>Toggle bookmark</button>
      </td>
    </tr>
  );
};
