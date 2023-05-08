export class UnknownError extends Error {
  constructor() {
    const message = 'Unknown error';
    super(message);
    this.name = 'UnknownError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
}

export class InvalidHttpUrlError extends Error {
  constructor() {
    const message = 'Invalid HTTP URL error';
    super(message);
    this.name = 'InvalidHttpUrlError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
};
