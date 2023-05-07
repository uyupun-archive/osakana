import { FunctionalComponent } from 'preact'
import { useEffect, useState } from 'preact/hooks'
import { ping } from '../../api/ping'
import LogoWithText from '../../assets/logo-with-text.svg'
import './home.css'

export function Home() {
  // const [count, setCount] = useState(0)

  useEffect(() => {
    (async () => {
      const res = await ping();
      console.log(res);
    })();
  }, []);

  return (
    <>
      <img src={LogoWithText} alt="Osakana logo with text" width="500" />
      <div>
				<input type="text" placeholder="https://..." />
				<button type="button">Add</button>
			</div>
      <div>
				<input type="text" placeholder="Keyword" />
				<button type="button">Search</button>
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
            title="TestTestTestTestTest"
            url="https://preactjs.com/tutorial/"
            created_at={new Date()}
            read_at={new Date()}
          />
				</tbody>
			</table>
    </>
  )
}

type HttpUrl = string;

interface ReadingListRecordProps {
  title: string;
  url: HttpUrl;
  created_at: Date;
  read_at: Date | null;
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
