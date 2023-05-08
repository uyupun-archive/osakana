import { FunctionalComponent, JSX } from 'preact';
import { useState } from 'preact/hooks';

import { searchReadingList } from '../../api/readingList';
import { ReadingListRecord as ReadingListRecordProps } from '../../types/index';
import LogoWithText from '../../assets/logo-with-text.svg';
import './home.css';

export const Home = (): JSX.Element => {
  const [inputSearchForm, setInputSearchForm] = useState('');

  const handleInputSearchForm = (e: Event): void => {
    const target = e.target as HTMLInputElement;
    setInputSearchForm(target.value);
  };

  const searchReadingListRecord = async (): Promise<void> => {
    const keyword = inputSearchForm;
    const res = await searchReadingList(keyword);
    console.log(res);
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
      <table border="1">
        <thead>
					<tr>
						<th>Title</th>
            <th>Created at</th>
            <th>Read at</th>
						<th>Action</th>
					</tr>
				</thead>
        <tbody>
          <ReadingListRecord
            id="b1562c9b-d21e-49de-91d1-aa766922fa51"
            url="https://github.com/uyupun"
            title="TestTestTestTestTest"
            is_read={false}
            thumb="https://github.githubassets.com/favicons/favicon.png"
            created_at={new Date()}
            updated_at={new Date()}
            read_at={new Date()}
          />
				</tbody>
			</table>
    </>
  );
};

const ReadingListRecord: FunctionalComponent<ReadingListRecordProps> = (props) => {
  return (
    <tr>
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
