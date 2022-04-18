/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /* 
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',
        
        /* 
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
            'registration-title': '#3B583B',
            'form-label': '#575641',
            'button': '#CEDCD3',
            'primary': '#D6D4A1',
            'shadow': '#bdbb74',
            'primary-border': '#BFBD87',
            'btn-pressed': '#C4D8C4',
            'btn-shadow': '#5D6C5D',
            'btn': '#99A799',
            'leaderboard-info': '#646464',
            'text-dark': '#141313',
            'container': '#F7F6E5',
            'container-blunt': '#F1F0DF',
            'purple': {
                2: "#363CB5",
                1: "#7B7FE8",
            },
            'pomodoro': {
                1: '#A4B3A4',
                2: '#7E967E',
                3: '#F7F6ED',
            },
            },
          dropShadow:{
            'btn-small': '0 2px 0 rgba(93, 108, 93, 1)',
            'btn-large': '0 3px 0 rgba(93, 108, 93, 1)',
            'btn-pending': '0 3px 0 rgba(54, 60, 181, 1)',
            'btn-red': '0 2px 0 rgba(220, 38, 38, 1)',
          },
            boxShadow:{
                'custom': '0px 1px 33px rgba(189, 187, 116, 0.15)'
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
