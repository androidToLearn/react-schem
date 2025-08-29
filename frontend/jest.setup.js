/// jest.setup.js
const { TextEncoder, TextDecoder } = require('util');
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

// Mocking fetch
global.fetch = () => Promise.resolve({
    json: () => Promise.resolve({ data: 'mocked data' }),
});