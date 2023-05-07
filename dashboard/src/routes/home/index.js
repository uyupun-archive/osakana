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
					<tr>
						<td>
							<a href="https://preactjs.com/tutorial/" target="_blank" rel="noreferrer noopener">TestTestTestTestTest</a>
						</td>
						<td>
							<button type="button">Read</button>
							<button type="button">Delete</button>
						</td>
					</tr>
				</tbody>
			</table>
			<section>
				<Resource
					title="Learn Preact"
					description="If you're new to Preact, try the interactive tutorial to learn important concepts"
					link="https://preactjs.com/tutorial/"
				/>
			</section>
		</div>
	);
};

const Resource = props => {
	return (
		<a href={props.link}>
			<h2>{props.title}</h2>
			<p>{props.description}</p>
		</a>
	);
};

export default Home;
