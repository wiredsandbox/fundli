from decouple import config



PORT = config('PORT', default = 7000, cast = int)