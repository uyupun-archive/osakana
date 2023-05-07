import { h } from 'preact';

const Home = () => {
	return (
		<div>
			<img src="../../assets/logo-with-text.svg" alt="Osakana logo with text" width="300" />
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
						<th>Action</th>
					</tr>
				</thead>
				<tbody>
					<ReadingListRecord title="TestTestTestTestTest" url="https://preactjs.com/tutorial/" />
				</tbody>
			</table>
		</div>
	);
};

const ReadingListRecord = props => {
	return (
		<tr>
			<td>
				<a href={props.url} target="_blank" rel="noreferrer noopener">{props.title}</a>
			</td>
			<td>
				<button type="button">Read</button>
				<button type="button">Delete</button>
			</td>
		</tr>
	);
};

export default Home;
