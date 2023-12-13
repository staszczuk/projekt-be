package org.example;

import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class PrestaShopTest {

    private static final String DEFAULT_LINK = "https://localhost:8443";
    private static final String PRODUCT_TO_FIND = "test";
    private static final String REGISTER_EMAIL = "s191005@gmail.com";

    public static void main(String[] args) {
        ChromeOptions chromeOptions = new ChromeOptions();
        chromeOptions.addArguments("--ignore-ssl-errors=yes");
        chromeOptions.addArguments("--ignore-certificate-errors");
        chromeOptions.addArguments("--start-maximized");
        chromeOptions.setExperimentalOption("detach", true);

        WebDriver driver = new ChromeDriver(chromeOptions);

        long startTime = System.currentTimeMillis();
        runTest(driver);
        long timeSpent = (System.currentTimeMillis() - startTime) / 1000;
        System.out.println("minutes : " + timeSpent / 60 + ", seconds : " + timeSpent % 60);

        driver.quit();
    }

    private static void add_to_cart(WebDriver driver, int amount) {
        WebElement add = driver.findElement(By.cssSelector("#add-to-cart-or-refresh > div.product-add-to-cart.js-product-add-to-cart > div > div.qty > div > span.input-group-btn-vertical > button.btn.btn-touchspin.js-touchspin.bootstrap-touchspin-up"));

        for (int i = 0; i < amount - 1; i++) {
            add.click();
        }

        driver.findElement(By.cssSelector("#add-to-cart-or-refresh > div.product-add-to-cart.js-product-add-to-cart > div > div.add > button")).click();
    }

    private static void delete_from_cart(WebDriver driver, int amount) {
        for (int i = 0; i < amount; i++) {
            driver.findElement(By.cssSelector("#_desktop_cart > div > div > a")).click();
            driver.findElement(By.cssSelector("#main > div > div.cart-grid-body.col-xs-12.col-lg-8 > div > div.cart-overview.js-cart > ul > li > div > div.product-line-grid-right.product-line-actions.col-md-5.col-xs-12 > div > div.col-md-2.col-xs-2.text-xs-right > div > a")).click();
        }
    }

    private static void register_user(WebDriver driver) {
        driver.findElement(By.cssSelector("#_desktop_user_info > div > a > span")).click();
        driver.findElement(By.cssSelector("#content > div > a")).click();
        driver.findElement(By.cssSelector("#field-id_gender-1")).click();
        driver.findElement(By.cssSelector("#field-firstname")).sendKeys("Jan");
        driver.findElement(By.cssSelector("#field-lastname")).sendKeys("Kowalski");
        driver.findElement(By.cssSelector("#field-email")).sendKeys("s191005@student.edu.gda.pl");
        driver.findElement(By.cssSelector("#field-password")).sendKeys("password");
        driver.findElement(By.cssSelector("#customer-form > div > div:nth-child(8) > div.col-md-6 > span > label > input[type=checkbox]")).click();
        driver.findElement(By.cssSelector("#customer-form > div > div:nth-child(10) > div.col-md-6 > span > label > input[type=checkbox]")).click();
        driver.findElement(By.cssSelector("#customer-form > footer > button")).click();
    }

    private static void runTest(WebDriver driver) {
        driver.get(DEFAULT_LINK);

        int[] amounts = {3, 2, 1, 2, 3, 1, 3, 2, 1, 1};
        int amountsIndex = 0;

        /*

        //Dodanie do koszyka 10 produktów
        for (int j : new int[]{5, 30}) {
            WebElement menu = driver.findElement(By.cssSelector("#_desktop_top_menu > ul.top-menu > li.category > a"));
            WebElement submenu = driver.findElement(By.cssSelector("#category-" + j + " > a"));

            Actions actions = new Actions(driver);
            actions.moveToElement(menu).click(submenu).perform();

            for (int i = 1; i < 7; i++) {
                int productIndex = (j == 5) ? i : i + 1;
                productIndex = (j == 5 && i >= 5) ? productIndex + 1 : productIndex;

                driver.findElement(By.cssSelector("#js-product-list > div.products.row > div:nth-child(" + productIndex + ") > article > div > div.thumbnail-top > a > img")).click();
                add_to_cart(driver, amounts[amountsIndex]);
              //  driver.findElement(By.cssSelector(".cart-content-btn button.btn-secondary")).click();
                driver.navigate().back();
                driver.navigate().back();
                amountsIndex++;

                if (j == 30 && i == 4) {
                    break;
                }
            }
        }
         */

        //Wyszukanie produktu po nazwie i dodanie do koszyka losowego produktu spośród znalezionych
        driver.findElement(By.cssSelector("#search_widget > form > input.ui-autocomplete-input")).sendKeys(PRODUCT_TO_FIND, Keys.RETURN);
        driver.findElement(By.cssSelector("#js-product-list > div.products.row > div:nth-child(2) > article > div > div.thumbnail-top > a > img")).click();
        add_to_cart(driver, 1);
        driver.navigate().back();
        driver.navigate().back();

        //Usunięcie z koszyka 3 produktów
        //delete_from_cart(driver, 1);

        //Rejestracja nowego konta
        register_user(driver);

        //Wykonanie zamówienia zawartości koszyka
        driver.findElement(By.cssSelector("#_desktop_cart > div > div > a > span.hidden-sm-down")).click();
        driver.findElement(By.cssSelector("#main > div > div.cart-grid-right.col-xs-12.col-lg-4 > div.card.cart-summary > div.checkout.cart-detailed-actions.js-cart-detailed-actions.card-block > div > a")).click();

        //Wybór metody płatności: przy odbiorze
        driver.findElement(By.cssSelector("#field-address1")).sendKeys("qwerty");
        driver.findElement(By.cssSelector("#field-postcode")).sendKeys("12-345");
        driver.findElement(By.cssSelector("#field-city")).sendKeys("Gdansk");
        driver.findElement(By.cssSelector("#delivery-address > div > footer > button")).click();

        java.time.Duration timeoutDuration = java.time.Duration.ofSeconds(10);
        //Wybór jednego z dwóch przewoźników:
        WebDriverWait wait = new WebDriverWait(driver, timeoutDuration);
        wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("#js-delivery > button"))).click();

        //Zatwierdzenie zamówienia
        driver.findElement(By.cssSelector("#payment-option-2")).click();
        driver.findElement(By.cssSelector("#conditions_to_approve[terms-and-conditions]")).click();

        driver.findElement(By.cssSelector("#payment-confirmation > div.ps-shown-by-js > button")).click();

        //Sprawdzenie statusu zamówienia
        driver.findElement(By.cssSelector("#_desktop_user_info > div > a.account > span")).click();
        driver.findElement(By.cssSelector("#history-link > span > i")).click();

        //Pobranie faktury VAT
        driver.findElement(By.cssSelector("#content > table > tbody > tr > td.text-sm-center.hidden-md-down > a")).click();
    }
}
