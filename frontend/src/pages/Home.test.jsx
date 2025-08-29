import Home from "./Home";
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';




test('home', async () => {
    //success home page test
    const { container } = render(<MemoryRouter><Home /></MemoryRouter>);

    await waitFor(() => {
        expect(container.querySelector('.allContent')).toBeInTheDocument();
        console.log('הפרטים מופיעים בעמוד Home')
    });

});

test('homeFailing', async () => {
    //failed home page test
    const { container } = render(<MemoryRouter><Home /></MemoryRouter>);

    await waitFor(() => {
        let p1 = container.querySelector('.p1')

        if (!p1) {
            console.log('טקסט p1 לא מופיע בhome page')
        }

    });
});