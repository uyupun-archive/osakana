import { FunctionalComponent, JSX } from 'preact';
import { useState } from 'preact/hooks';

import {
  addReadingListRecord,
  searchReadingList,
  fetchFeelingReadingListRecord,
  readReadingListRecord
} from '../../api/endpoints/readingList';
import type { Uuid4, ReadingList, ReadingListRecord as ReadingListRecordProps } from '../../types';
import { InvalidHttpUrlError } from '../../errors';
import { ReadingListRecordTypeError, UrlNotFoundError, UrlAlreadyExistsError, ReadingListRecordAlreadyReadError } from '../../api/errors';
import LogoWithText from '../../assets/logo-with-text.svg';
import NoImage from '../../assets/no-image.svg';
import './home.css';

export const Home = (): JSX.Element => {
  const [inputAddForm, setInputAddForm] = useState<string>('');
  const [inputAddFormMessage, setInputAddFormMessage] = useState<string | null>(null);
  const [inputSearchForm, setInputSearchForm] = useState<string>('');
  const [inputSearchErrorMessage, setInputSearchErrorMessage] = useState<string | null>(null);
  const [readingList, setReadingList] = useState<ReadingList>([]);

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
    try {
      const res = await searchReadingList(keyword);
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

  const handleFeelingReadingListRecord = async (): Promise<void> => {
    try {
      const res = await fetchFeelingReadingListRecord();
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
				<button type="button" onClick={handleFeelingReadingListRecord}>Feeling</button>
        {inputSearchErrorMessage && <div>{inputSearchErrorMessage}</div>}
			</div>
      {readingList.length <= 0 && <p>No records</p>}
      {readingList.length > 0 && (
        <table border="1">
          <thead>
            <tr>
              <th>Icon</th>
              <th>Title</th>
              <th>Created at</th>
              <th>Is read</th>
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
                thumb={readingListRecord.thumb}
                createdAt={readingListRecord.createdAt}
                updatedAt={readingListRecord.updatedAt}
                readAt={readingListRecord.readAt}
                onRead={handleSearchReadingList}
              />
            ))}
          </tbody>
        </table>
      )}
    </>
  );
};

const ReadingListRecord: FunctionalComponent<ReadingListRecordProps & {onRead: () => Promise<void>}> = (props) => {
  const handleReadReadingListRecord = async (id: Uuid4): Promise<void> => {
    try {
      await readReadingListRecord(id);
    } catch (e: unknown) {
      if (e instanceof ReadingListRecordAlreadyReadError) {
        console.log(e.message);
        return;
      }
      console.log('Unknown error');
    }
  };

  return (
    <tr>
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
        {!props.isRead && <button type="button" onClick={async () => {
          await handleReadReadingListRecord(props.id);
          await props.onRead();
        }}>Read</button>}
        {props.isRead && <button type="button" onClick={() => console.log("Unread")}>Unread</button>}
        <button type="button" onClick={() => console.log("Delete")}>Delete</button>
      </td>
    </tr>
  );
};
