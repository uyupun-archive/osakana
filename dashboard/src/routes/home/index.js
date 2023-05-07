import { h } from 'preact';

const Home = () => {
	return (
		<div>
			<img src="../../assets/logo-with-text.svg" alt="Osakana logo with text" width="300" />
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
