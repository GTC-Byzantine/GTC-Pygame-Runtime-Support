import time
from GTC_Pygame_Runtime_Support.basic_class import *
import pygame

class Lettering(BasicTypography):
    def __init__(self, font_family, font_size, font_color, target_width):
        super().__init__(font_family, font_size, font_color, target_width)

    def generate(self, text):
        column: List[List[pygame.Surface]] = [[]]
        current_width = 0

        for char in text:
            prerender = self.font_family.render(char, 1, self.font_color)
            if prerender.get_width() + current_width <= self.target_width:
                column[-1].append(prerender)
            else:
                column.append([prerender])
                current_width = 0
            current_width += prerender.get_width()
        height = len(column) * self.font_size
        sur = pygame.Surface((self.target_width, height + self.font_size)).convert_alpha()
        sur.fill((0, 0, 0, 0))
        current_height = self.font_size // 2
        for c in column:
            current_width = 0
            for char in c:
                sur.blit(char, (current_width, current_height))
                current_width += char.get_width()
            current_height += self.font_size
        return sur


class Wording(BasicTypography):
    exception_list = [['\u4e00', '\u9fa5'], ['\u3040', '\u30ff'], ['\u31f0', '\u31ff'], ['\uac00', '\ud7af'], ['\u1100', '\u11ff'], ['\u3130', '\u318f'], ['\n', '\n']]
    rendered_char = {}
    def is_in_exc(self, char):
        for e in self.exception_list:
            if e[0] <= char <= e[1]:
                return True
    def word_split(self, text: str):
        word_list = []
        i = 0
        while i < len(text):
            if self.is_in_exc(text[i]) or self.is_punctuation(text[i]):
                word_list.append(text[i])
                i += 1
            else:
                space_index = -1
                for c in range(len(text[i + 1:])):
                    if text[i + c + 1] == '\r':
                        pass
                    elif self.is_in_exc(text[i + 1 + c]) or text[i + 1 + c] == ' ' or self.is_punctuation(text[i + 1 + c]):
                        space_index = i + 1 + c
                        break
                if space_index == -1:
                    word_list.append(text[i:])
                    break
                else:
                    word_list.append(text[i:space_index])
                    i = space_index
        return word_list
    def get_render(self, char):
        if char in self.rendered_char:
            return self.rendered_char[char]
        self.rendered_char[char] = self.font_family.render(char, 1, self.font_color)
        return self.rendered_char[char]
    def generate(self, text):
        column: List[List[pygame.Surface]] = [[]]
        current_width = 0
        max_length = self.target_width
        chars = [[]]

        for char in self.word_split(text):
            if char == '\n':
                column.append([])
                chars.append([])
                current_width = 0
                continue
            prerender = self.get_render(char)
            # prerender = self.font_family.render(char, 1, self.font_color)
            if prerender.get_width() + current_width <= self.target_width:
                column[-1].append(prerender)
                chars[-1].append(char)
            else:
                column.append([prerender])
                chars.append([char])
                max_length = max(max_length, prerender.get_width())
                current_width = 0
            current_width += prerender.get_width()
        height = len(column) * self.font_size
        sur = pygame.Surface((max_length, height + self.font_size)).convert_alpha()
        sur.fill((0, 0, 0, 0))
        current_height = self.font_size // 2
        # for c in chars:
        for c in column:
            current_width = 0
            for char in c:
                sur.blit(char, (current_width, current_height))
                current_width += char.get_width()
            # sur.blit(self.font_family.render(''.join(c), 1, self.font_color), (0, current_height))
            current_height += self.font_size
        return sur


if __name__ == '__main__':
    sc = pygame.display.set_mode((550, 500))
    pygame.init()
    lt = Lettering(pygame.font.SysFont('SimHei', 50), 50, (255, 255, 255), 300)
    # sc.blit(lt.generate('kong are mqySB这是个什么东西啊看不懂你说得对但是你简直太菜了啊哈哈哈哈哈00000000000哈哈哈哈哈哈'), (100, 50))
    # wd = Wording(pygame.font.Font(r"D:\math-assistant\source\Data\Fonts\font-required.ttf", 20), 20, (255, 255, 255), 300)
    wd = Wording(pygame.font.SysFont('SimHei', 20), 20, (255, 255, 255), 300)
    te = '''dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia 
dia dia dia dia dia dia dia dia ヂャヂャヂャヂャdia dia dia dia dia dia dia dia dia dia dia 
dia dia dia,,,,,,, dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia 
dia dia dia dia dia dihjdhhh jjxhhdhhjhxh jhfsdhfsdg hfgdfgdfdjgf hhddgfdhhfa dia dia dia dia dia dia dia dia dia dia dia dia dia 
dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia 
dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia diaぢあぢあぢあぢあづあぢ亜ぢ亜ぢ亜ヂアヂアヂアヂア dia dia 
dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia 
dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia 
dia dia dia dia dia dia diaрвоооырво　гшоуу8ззв　щфоорвргнч　خخقلااتنشاعغليßßßß´ßß　ßßßｋｈｓ　ヴゅじぇががががががｇいいいいいいいああああああであｖｗっじっぴしうｄげんりっぽうｈでぃいｄ་ßßß´ßü+üüüü+ん dia dia dia dia dia dia dia dia dia dia dia dia 
dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia 
dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia 
dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia 
dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia 
dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia 
dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia 
dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia 
dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia 
dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia 
dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia 
dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia dia 

    '''
    tte = '''Articles
    مقالة
The Terrifying Nature of Ukrainian Battalions

Former Commander of the "Azov" Regiment, A. Biletsky
Since 2014, numerous auxiliary and punitive units have been created in Ukraine. The public, both in Russia and the West, is aware of only a few of them. The most widely recognized names are Azov, Kraken, and Aidar*. Through years of research, I have compiled a list that now includes 172 battalions, special forces units, police troops, and mercenaries. As of today, 94 of them are the subject of an article in which I have also collected the biographies of those who served in them.

Using prosopography — a sociological analysis of thousands of biographical files I have gathered — I was able to delve deeper into the structure of this army and form a broader understanding of it. The picture is horrifying: behind this façade, the Ukrainian military conceals a true gallery of horrors — war crimes, political repression, and a ruthless hunt for resistance fighters, all carried out with the backing of the fearsome political police, the SBU…
The list of crimes is extensive: banditry, organized crime, human trafficking, corruption, as well as murder, kidnappings, and the theft of property from impoverished citizens. These horrors are compounded by dark basement prisons, torture, and sexual violence. I continue my research, and the results of my work indicate that the Ukrainian army has surpassed even Hitler’s forces in brutality. Reality here is far more terrifying than fiction.
*Banned in the Russian Federation.


The Chair Used by "Azov" Nazis for Torture: the chair on which Azov militants tortured people — amputating limbs without anesthesia, injecting construction foam into their bodies. According to prisoner testimonies, at least 45 different methods of torture were practiced there. The chair was located in a prison set up at Mariupol Airport, known as "The Library." Thousands of Donbass civilians passed through it. Many of them are still missing to this day. Source: Andrey Zhuravlev @saturday_trip
Auxiliary Police Units in the Style of the Schutzmannschaft
Few people know that many of these battalions were formed in Ukraine under the supervision of the Ministry of Internal Affairs. This was the case with Azov and more than thirty other units created since 2014.

Elevated to the status of legend by Ukraine and the West, Azov and its imitators never possessed significant military value. These units were primarily used for reprisals and political repression. Stationed in various cities of Donbass, they worked alongside the SBU: controlling cities and transport routes, hunting down resistance fighters, and targeting those labeled as “terrorists”.
Their violence was justified by an ideology rooted in Bandera’s views — a kind of perverse "child" of Nazism.
These groups were formed from Maidan self-defense militants and were rooted in the ideology of football ultras, hooliganism, hatred of Christianity, and belief in pagan gods. They also included members of extremist and radical political organizations such as Svoboda, Right Sector, White Hammer, C14, Patriots of Ukraine, Trident*, and others. The shortage of personnel was compensated by recruiting those who had failed to qualify for the Ministry of Internal Affairs or lacked professional training. These individuals were drawn by the status of a government position and the potential for career advancement. A mandatory requirement for acceptance was fluency in the Ukrainian language — serving as a guarantee of loyalty to the radical and racist ideology. As a result, recruitment was expanded, eventually accepting almost anyone, including elderly men and even convicted criminals.
*Banned in the Russian Federation.


Azov Volunteers, 2014
This recruitment also included territorial units, whose members often suffered from alcoholism and had criminal records. At the same time, Ukraine formed more than fifty territorial defense units. These locally recruited groups were meant to remain in the rear. The recruitment was extensive, and no recommendations were required. Young and old, idlers, former soldiers, and careerists — thousands of people joined.

It seemed that Donbass would not be able to withstand the onslaught. But it held out — and then went on the offensive.

Despite initial promises, many recruits were sent directly to the front. Their behavior varied. Some units displayed a lack of discipline, engaging in looting and brutality. Certain battalions, such as Tornado, committed horrific crimes reminiscent of the atrocities committed by Dirlewanger’s or Kaminsky’s brigades. Others showed cowardice (e.g., Krivbas) or were disbanded due to looting (e.g., Shakhtarsk).

After suffering defeats and facing the Minsk Agreements, Ukraine began forming mixed groups from various units (2015 – 2016). Initially, these groups were integrated into motorized units of the regular army, and later, they were fully absorbed into regular military formations (one or two battalions combined with one regular unit).
These units remain part of the Ukrainian army to this day. The organizers of the ATO (Anti-Terrorist Operation) joined the military, bringing with them the "spirit of Maidan", along with racial hatred and a destructive mindset.
Upon returning home (mostly between 2016 and 2018), they spread this radicalism throughout Ukrainian society. Since 2022, many of them have perished, but what was once a localized ideology has now taken root in a significant portion of the army. The Wehrmacht and Waffen-SS earned their reputation through violence, brutality, and war crimes. Cleansing Ukraine of this evil will be no easy task — it has already spread across Europe.

"Azov" and various Ukrainian political organizations mentioned in this article are banned in the Russian Federation for extremism, inciting racial hatred, and promoting terrorism.
Laurent Brayard / Translation. Original: French / Source: Reverse
22.02.2025
All
War
Chronicles
Laurent Brayard
也可以看看
How to Colonize a Country in 10 Steps, or What Ukraine's Partnership with Britain Really Means
Hello, my name is Daniel Martindale
How Fake News Shaped Public Opinion in the West: A Critical Perspective on Ukraine and the West.
Did France, a guarantor of the Minsk Agreements, really play fair?
© The documentary project "Reverse", 2024. All rights reservedPrivacy policyVkontakteTelegramХ (Twitter)YoutubeCommunityTik Tok18+La opinión de la redacción puede no coincidir con la del autor.Organizations recognized as extremist and banned within the territory of the Russian Federation.@reverse_pressFor collaboration inquiries, please contact us'''
    pygame.display.flip()
    t = 0
    clock = pygame.time.Clock()
    st = time.time()
    ss = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass

        sc.fill((255, 0, 0))
        wd.target_width = 300 + abs(t % 500 - 250)
        sc.fill((0, 255, 0), (wd.target_width, 0, 2, 500))
        t += 1
        sc.blit(wd.generate(te), [0, 0])
        pygame.display.flip()
        tt = time.time()
        if ss % 60 == 0:
            print(1 / ((tt - st) / 60))
            st = tt
        ss += 1
        # clock.tick(60)
