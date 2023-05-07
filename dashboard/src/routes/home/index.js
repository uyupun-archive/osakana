import { h } from 'preact';

const Home = () => {
	return (
		<div>
			<img src="../../assets/logo.svg" alt="Osakana Logo" height="160" width="160" />
			<h1>Osakana</h1>
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
