export class ValidationError extends Error {
  constructor() {
    const message = 'Validation error';
    super(message);
    this.name = 'ValidationError';
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

export class ReadingListCountsTypeError extends Error {
  constructor() {
    const message = 'ReadingListCounts type error';
    super(message);
    this.name = 'ReadingListCountsTypeError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
};

export class ExportReadingListRecordTypeError extends Error {
  constructor() {
    const message = 'ExportReadingListRecord type error';
    super(message);
    this.name = 'ExportReadingListRecordTypeError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
};

export class EmptyFileError extends Error {
  constructor() {
    const message = 'Empty file error';
    super(message);
    this.name = 'EmptyFileError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
};

export class FileSizeLimitExceededError extends Error {
  constructor() {
    const message = 'File size limit exceeded error';
    super(message);
    this.name = 'FileSizeLimitExceededError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
};

export class InvalidFileExtensionError extends Error {
  constructor() {
    const message = 'Invalid file extension error';
    super(message);
    this.name = 'InvalidFileExtensionError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
};

export class InvalidJsonContentsError extends Error {
  constructor() {
    const message = 'Invalid JSON contents error';
    super(message);
    this.name = 'InvalidJsonContentsError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
};

export class InvalidJsonStructureError extends Error {
  constructor() {
    const message = 'Invalid JSON structure error';
    super(message);
    this.name = 'InvalidJsonStructureError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
};

export class ExportReadingListRecordParseError extends Error {
  constructor() {
    const message = 'Export reading list record parse error';
    super(message);
    this.name = 'ExportReadingListRecordParseError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
};

export class ReadingListRecordDuplicateError extends Error {
  constructor() {
    const message = 'Reading list record duplicate error';
    super(message);
    this.name = 'ReadingListRecordDuplicateError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
};
