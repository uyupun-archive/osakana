export class UrlNotFoundError extends Error {
  constructor() {
    const message = 'URL not found error';
    super(message);
    this.name = 'UrlNotFoundError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
};

export class UrlAlreadyExistsError extends Error {
  constructor() {
    const message = 'URL already exists error';
    super(message);
    this.name = 'UrlAlreadyExistsError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
};

export class ReadingListRecordTypeError extends Error {
  constructor() {
    const message = 'ReadingListRecord type error';
    super(message);
    this.name = 'ReadingListRecordTypeError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
};

export class ReadingListRecordNotFoundError extends Error {
  constructor() {
    const message = 'ReadingListRecord not found error';
    super(message);
    this.name = 'ReadingListRecordNotFoundError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
}

export class ReadingListRecordAlreadyReadError extends Error {
  constructor() {
    const message = 'ReadingListRecord already read error';
    super(message);
    this.name = 'ReadingListRecordAlreadyReadError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
};

export class ReadingListRecordNotYetReadError extends Error {
  constructor() {
    const message = 'ReadingListRecord not yet read error';
    super(message);
    this.name = 'ReadingListRecordNotYetReadError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
};
