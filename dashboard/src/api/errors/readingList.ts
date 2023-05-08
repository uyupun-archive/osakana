export class ReadingListRecordTypeError extends Error {
	constructor() {
		const message = 'ReadingListRecord type error';
		super(message);
		this.name = 'ReadingListRecordTypeError';
		Object.setPrototypeOf(this, new.target.prototype);
	};
};
