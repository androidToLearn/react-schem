export default {
    transform: {
        '^.+\\.[tj]sx?$': 'babel-jest',
    },
    moduleNameMapper: {
        '\\.(css|less|sass|scss)$': 'identity-obj-proxy',
        '\\.(gif|ttf|eot|svg|png|jpg|jpeg|webp)$': '<rootDir>/mocks/fileMock.js',
    },
    testEnvironment: 'jsdom',
    setupFiles: ['<rootDir>/jest.setup.js'],  // הרצת קוד לפני כל הטסטים
};
