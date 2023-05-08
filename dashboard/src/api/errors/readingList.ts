export class ReadingListRecordTypeError extends Error {
  constructor() {
    const message = 'ReadingListRecord type error';
    super(message);
    this.name = 'ReadingListRecordTypeError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
};

export class UrlNotFoundError extends Error {
  constructor() {
    const message = 'URL not found error';
    super(message);
    this.name = 'UrlNotFoundError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
}

export class UrlAlreadyExistsError extends Error {
  constructor() {
    const message = 'URL already exists error';
    super(message);
    this.name = 'UrlAlreadyExistsError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
}
