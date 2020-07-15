import { Component, OnInit } from '@angular/core'
import { SearchService } from './search.service'
import { Rss } from '../rss/rss'

declare let alertify: any

@Component({
    selector: 'app-search',
    templateUrl: './search.component.html',
})

export class SearchComponent {

    pageCurrent: number = 1
    constructor(private searchService:SearchService) { }

    dates =  {
        start_date:Date,
        end_date: Date
    }

    rss:Rss[]

    ngOnInit(){
    }

    search() {
        if(this.dates.start_date < this.dates.end_date){
            this.searchService.getRssWithDate(this.dates).subscribe(
                res =>{
                    if(res){
                        this.rss = res
                    }
                }
            )
        }else{
            alertify.warning('start date must be smaller than end date')
        }
    }
}
