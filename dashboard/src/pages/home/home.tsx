import { FunctionalComponent, JSX } from 'preact';
import { useState } from 'preact/hooks';

import { searchReadingList, ReadingListRecordTypeError } from '../../api/readingList';
import type { ReadingList, ReadingListRecord as ReadingListRecordProps } from '../../types/index';
import LogoWithText from '../../assets/logo-with-text.svg';
import NoImage from '../../assets/no-image.svg';
import './home.css';

export const Home = (): JSX.Element => {
  const [inputSearchForm, setInputSearchForm] = useState<string>('');
  const [readingList, setReadingList] = useState<ReadingList>([]);
  const [readingListErrorMessage, setReadingListErrorMessage] = useState<string | null>(null);

  const handleInputSearchForm = (e: Event): void => {
    const target = e.target as HTMLInputElement;
    setInputSearchForm(target.value);
  };

  const handleSearchReadingList = async (): Promise<void> => {
    const keyword = inputSearchForm;
    try {
      const res = await searchReadingList({keyword: keyword});
      setReadingListErrorMessage(null);
      setReadingList(res);
    } catch (e: unknown) {
      if (e instanceof ReadingListRecordTypeError) {
        setReadingListErrorMessage(e.message);
        return;
      }
      setReadingListErrorMessage('Unknown error');
    }
  };

  return (
    <>
      <img src={LogoWithText} alt="Osakana logo with text" width="500" />
      <div>
				<input type="text" placeholder="https://..." />
				<button type="button">Add</button>
			</div>
      <div>
				<input type="text" placeholder="Keyword" value={inputSearchForm} onChange={handleInputSearchForm} />
				<button type="button" onClick={handleSearchReadingList}>Search</button>
				<button type="button">Feeling</button>
			</div>
      {readingListErrorMessage && <p>{readingListErrorMessage}</p>}
      {readingList.length <= 0 && <p>No records</p>}
      {readingList.length > 0 && (
        <table border="1">
          <thead>
            <tr>
              <th>Icon</th>
              <th>Title</th>
              <th>Created at</th>
              <th>Read at</th>
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
              />
            ))}
          </tbody>
        </table>
      )}
    </>
  );
};

const ReadingListRecord: FunctionalComponent<ReadingListRecordProps> = (props) => {
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
      <td>{props.readAt?.toLocaleString()}</td>
      <td>
        <button type="button" onClick={() => console.log("Read")}>Read</button>
        <button type="button" onClick={() => console.log("Delete")}>Delete</button>
      </td>
    </tr>
  );
};
