# Nonograms.org archive project

  

## Background

I love nonograms, those japanese 'crosswords', sometimes called Picross', I've done a lot of them, and it's always a pleasure to challenge myself.  
  
Anyway, there's a cool website out there that lets users create nonograms for everyone to play, they come in flavors too ! black and white, colored ones, animals, adult ones, landscapes, really neat.  
  
They got a ton too, I think the website has been around since 2009, it adds up to (at the time of writing this (2024/11)) around 60k.  
  
More and more these days we talk about how important archiving everything is, since when it's lost, it's lost. I think it'd be a shame if for whatever reason this website goes down, taking with it all the lovely nonograms created by the community along the years.  
  
Here's my humble contribution to prevent this from happening, and hey, it's quite a fun side project !

## Journey

Getting ideas is the easy part, getting things done is trickier, and the first and most important task is : is it even possible ?  
  
So I dug in to check what was possible to get easily, what wasn't and what was impossible.  

> Good news: nothing's impossible ✌️

  
Let's list things out:

*   Each nonogram has an id
    *   It's a straightforward integer going from 1 to infinity and beyond (lucky for us)
*   Each nonogram is accessible through a URI combination of a base then the id
    *   https://www.nonograms.org/nonograms/i/<id\>
    *   Even more lucky for us, no need to parse through the browse section 👌
*   The base URI comes in two flavors :
    *   https://www.nonograms.org/nonograms/i/<id\>
    *   https://www.nonograms.org/nonograms2/i/<id\>
        *   Notice this '2' hidden here ? It means it's a colored one (yeah for some reason they got different handles 🤷)
    *   Actual pages are sent by the server (probably with PHP) almost completed
    *   EXCEPT for the nonograms `<canvas>`, it's generated with JavaScript through some data passed inside a `<script>` tag (that's the core of this project, without it it'd be waaaay harder)
        *   More on that further down
    *   We get some neat data listed :
        *   nonogram id (already had)
        *   nonogram name
        *   author name
        *   author id (through href)
        *   is the nonogram tagged as 'adult' (+18)
*   If an id has no match, returns a 404 Response
    *   If I get one for B&W, I try with the Colored URI (nonograms2)
        *   Usually it's either one
*   If it has been deleted, a red warning appears to let us know
*   The upper maximum size seems to be 200x200

  
Quite the start ! We have a few data already, but not about the puzzle itself, so where is it ?  
  
Lucky for us, I found some data hidden inside a `<script>` tag :  
  
![Screenshot 2024-11-10 214630](https://github.com/user-attachments/assets/647bdb6c-3fcb-48ec-aa65-58546681ff3e)
  
This, is our goldmine, this `d` var has everything we need, but this raw data means nothing. At first, I tried to rack my brains and figure out what it could mean and how it should be read, no luck.  
  
Just after, we can see a script attached, some 'nonograms2.min.js' surely it holds our most desired answers to get our data !  
  
Fat luck again, it's all just a jumbled mess !  
It's a minified and / or obfuscated JavaScript, it's common to see them in the wild  
  
![image](https://github.com/user-attachments/assets/c7885160-de5f-4d85-921d-3fa204705b26)

However, do not fret over this, friends, as I have made this my life mission !  
After careful search, I noticed it used our lovely `d` var and pokes around with it to get some data.  
  
![image](https://github.com/user-attachments/assets/33e70245-8f41-4923-9372-2550c401c4b6)
  
Still an incomprehensible mess, but we're getting somewhere.  
It was clear I needed to reverse engineer it to at least get something tangible to use.  
  
The powerful debugger helped me understand bit by bit what was stored inside those anonymous variables, and after a few hours of back and forth trial and errors, here's an exhaustive list of what I found (pretty much everything) :

*   Fc : Nonogram ID
*   I : Column count
*   J : Row count
*   K : Color count (1 for B&W)
*   Gc : Colors list (hex codes)
*   $c : Completed answer grid
*   M : Non-empty consecutive cells in columns
*   N : Non-empty consecutive cells in rows
*   Jc : Column colors (to be mapped with M)
*   Kc : Row colors (to be mapped with N)  
  
Tedious but interesting task, I also had to simplify the messy code to something I could understand (and use).  
  
**To summarize** : our `d` var is a generated obfuscated matrix used alongside an algorithm by your browser to decode it into data it can use to generate the nonogram canvas.  
I transcribed their code to python until I had the $c (completed answer grid), with it, I could compute myself the consecutive cells and colors. (I couldn't wrap my head around how it was computed in the original code)  
  
You can see my last steps of reverse engineering the JavaScript part inside the 'reverse\_engineering.js' file.  
  
After a few more trial and errors I had a solid algorithm ready to go !

## Output format and size concerns

Now that I had every data I wanted, I could focus on the grand final : the 'archive' file itself.  
  
It's a file meant to be kept as is for quite some time after all, I want to keep relevant data only, and have a simple way to retrieve them.  
  
You can read some details inside the 'template.nono' file (it's the same header inside the archive) but the gist is:  
I kept:

*   Nonogram Id (from the website)
*   Nonogram Title
*   Nonogram Author Id (from the website)
*   Nonogram Author Name
*   Adult theme tag
*   Column Count
*   Row Count
*   Color Count
*   Color Codes
*   Non-empty consecutive cells in columns
*   Column colors (mapped to cons. cells)
*   Non-empty consecutive cells in rows
*   Row colors (mapped to cons. cells)

  
It's a semi-comma (;) separated values for each line and has everything needed to parse itself.  
  
Also, some values are skipped / 'nulled' when not needed or not given :

*   Author can be null (not user created I guess)
*   If Color Count is 1 (B&W)
    *   Colors codes
    *   Column colors
    *   Row colors
*   Adult theme tag (1 if true, else skipped)

  
Skipped means it's empty between the two semi commas (;), so when you parse it you still need to go through them.  
  
Obviously the heaviest ones are huge, colored, with lots of noise.  
  
I think I did my best to keep it as lightweight as possible, but I'd love to hear some feedbacks for things I could've done better !

### Update

It's now finished, the archive.nono file is a whooping 102MB file 🥳

It's not **that** heavy but still, I knew it could be squeezed more.

I played around a bit with compression algorithm like Zstd, Deflate, etc... And managed to keep its size down by -79.8% (20.6 MB) !

> The archive is compressed with 7Zip and the LZMA2 method

## Parsing

I implemented a simple parser in python (inside 'parser.py') you can use as is or as reference.
