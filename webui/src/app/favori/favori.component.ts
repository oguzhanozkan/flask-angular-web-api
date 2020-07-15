import { Component } from '@angular/core'
import { AuthenticationService } from '../authentication.service'
import { UserDetails } from '../UserDetails'
import { FavoriService } from './favori.service'
import { Rss } from '../rss/rss'

@Component({
  selector: 'app-favori',
  templateUrl: './favori.component.html'
})

export class FavoriComponent {
  

  constructor(private favoriService: FavoriService) { }

  rss: Rss[]

  ngOnInit() {
    this.favoriService.getFavoriRss().subscribe(
      rss => {
        if(rss){
          this.rss = rss
        }
      })
  }

  
}
