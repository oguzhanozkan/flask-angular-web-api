import { Injectable } from '@angular/core'
import { HttpClient} from '@angular/common/http'
import { Rss } from './rss'
import { Observable } from 'rxjs'
import {environment} from '../../environments/environment'


@Injectable()
export class RssService {
    constructor(private http:HttpClient) { }

    rss:Rss
    private RSS_PATH = "/rss"
    private GET_RSS_BY_ID = "/get_rss_by_id/"
    private ADD_ADDFAVORITE_RSS_PATH = "/rss_add_favorite/"

    
    getRssAll():Observable<Rss[]>{
        return this.http.get<Rss[]>(environment.API_BASE_PATH + this.RSS_PATH)
    }

    getRssById(id):Observable<Rss>{
        return this.http.get<Rss>(environment.API_BASE_PATH + this.GET_RSS_BY_ID + id)
    }
    
    addFavori(id,rss):Observable<any>{
        return this.http.post(environment.API_BASE_PATH +this.ADD_ADDFAVORITE_RSS_PATH + id, rss)
    }
}
