import { Rss } from "./rss/rss"

export class UserDetails {
    _id: string
    first_name: string
    last_name: string
    email: string
    password: string
    exp: number
    iat: number
    favori_rss:Rss[]
}