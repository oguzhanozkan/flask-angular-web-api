import { Injectable } from '@angular/core'
import { HttpClient} from '@angular/common/http'
import { Rss } from '../rss/rss'
import { Observable } from 'rxjs'
import {environment} from '../../environments/environment'
import { map } from 'rxjs/operators'


@Injectable()
export class FavoriService {
    constructor(private http:HttpClient) { }    

    rss:Rss

    private FAVORI_RSS = "/get_favorite_rss"

    getFavoriRss():Observable<Rss[]>{

        return this.http.get<Rss[]>(environment.API_BASE_PATH + this.FAVORI_RSS)
    }
}
