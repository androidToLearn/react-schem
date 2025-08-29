import Statistics from "./StatisticPage";
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';



test('statistics', async () => {
    //success statistics page
    const { container } = render(<MemoryRouter>
        <Statistics /></MemoryRouter>);

    await waitFor(() => {
        expect(container.querySelector('.content')).toBeInTheDocument();
        console.log('הפרטים מופיעים בעמוד Statistics')
    });
});

test('statisticsFailing', async () => {
    //failed statistics page
    const { container } = render(<MemoryRouter><Statistics /></MemoryRouter>);

    await waitFor(() => {
        let p1 = container.querySelector('.p1')
        if (!p1) {
            console.log('טקסט p1 לא מופיע ב statstics page')
        }
    });

});


