export class PingTypeError extends Error {
  constructor() {
    const message = 'Ping type error';
    super(message);
    this.name = 'PingTypeError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
};
