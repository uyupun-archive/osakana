import { FunctionalComponent, JSX } from 'preact';
import { useState } from 'preact/hooks';

import { searchReadingList } from '../../api/readingList';
import { ReadingList, ReadingListRecord as ReadingListRecordProps } from '../../types/index';
import LogoWithText from '../../assets/logo-with-text.svg';
import NoImage from '../../assets/no-image.svg';
import './home.css';

export const Home = (): JSX.Element => {
  const [inputSearchForm, setInputSearchForm] = useState('');
  const [readingList, setReadingList] = useState<ReadingList>([]);

  const handleInputSearchForm = (e: Event): void => {
    const target = e.target as HTMLInputElement;
    setInputSearchForm(target.value);
  };

  const searchReadingListRecord = async (): Promise<void> => {
    const keyword = inputSearchForm;
    const res = await searchReadingList(keyword);
    setReadingList(res);
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
				<button type="button" onClick={searchReadingListRecord}>Search</button>
				<button type="button">Feeling</button>
			</div>
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
                is_read={readingListRecord.is_read}
                thumb={readingListRecord.thumb}
                created_at={readingListRecord.created_at}
                updated_at={readingListRecord.updated_at}
                read_at={readingListRecord.read_at}
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
      <td>{props.created_at.toLocaleString()}</td>
      <td>{props.read_at?.toLocaleString()}</td>
      <td>
        <button type="button" onClick={() => console.log("Read")}>Read</button>
        <button type="button" onClick={() => console.log("Delete")}>Delete</button>
      </td>
    </tr>
  );
};
