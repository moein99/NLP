import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;

public class Scrapper
{
    public static void main(String[] args)
    {
        Path currentDir = Paths.get(System.getProperty("user.dir"));
        Path transAddr = Paths.get(currentDir.toAbsolutePath().toString(), "Transcripts/");
        File f = new File(transAddr.toAbsolutePath().toString());
        if (!f.exists())
        {
            f.mkdirs();
        }
        String url = "https://fangj.github.io/friends/";
        Document document, episodeDialogues;
        try
        {
            document = Jsoup.connect(url).get();
            Elements episodes = document.getElementsByTag("a");
            HashMap<String, String> episodeToLink = new HashMap<>();
            for (Element episode : episodes)
            {
                episodeToLink.put(episode.text(), episode.attr("href"));
            }
            for (String key : episodeToLink.keySet())
            {
                episodeDialogues = Jsoup.connect(url + episodeToLink.get(key)).get();
                Elements paragraphs = episodeDialogues.getElementsByTag("p");
                String season_episode = key.split(" ")[0];
                if (season_episode.contains("-"))
                {
                    season_episode = season_episode.replace(season_episode.substring(season_episode.indexOf('-'), season_episode.length()), "");
                }
                String seasonNumber = season_episode.substring(0, season_episode.length() - 2);
                File file = new File(Paths.get(transAddr.toAbsolutePath().toString(), "Season s#/ename.txt".replace("s#", seasonNumber).replace("ename", fixName(key))).toAbsolutePath().toString());
                file.getParentFile().mkdirs();
                try(FileWriter fw = new FileWriter(file, false);)
                {
                    for (Element paragraph : paragraphs)
                    {
                        fw.append(paragraph.text());
                        fw.append(String.format("%n"));
                    }
                }
                catch (IOException e)
                {
                    e.printStackTrace();
                }
            }
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    private static String fixName(String fileName)
    {
        String[] notAllowedWords = {"CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"};
        if (fileName.length() > 200)
        {
            fileName = fileName.substring(0,200);
        }
        fileName = fileName.replaceAll("[<>:\"/|?*]", "").replace("\\", "");
        for (String s : notAllowedWords)
        {
            if (fileName.contains(s))
            {
                fileName = fileName.replace(s, "");
            }
        }
        return fileName;
    }
}
